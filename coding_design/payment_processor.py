from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Set, Dict, ClassVar
from abc import ABC, abstractmethod
from threading import Lock, Thread
from enum import Enum
import time

GLOBAL_TIMEOUT = 300


class NoMatchingAccount(Exception):
    pass


class AmountExceedsBalance(Exception):
    pass


class ReceiverFailedToReceive(Exception):
    pass


class ExpiredTransaction(Exception):
    pass


class FailedTransaction(Exception):
    pass


class CriticalError(Exception):
    pass


class TransactionState(Enum):
    NEW = 1
    IN_PROGRESS = 2
    FAILED = 3
    COMPLETED = 4


class Account:
    def __init__(self, starting_balance: int, user: "User") -> None:
        self.balance = starting_balance
        self.user = user
        self.frozen: Dict["Transaction", datetime] = {}  # to remove
        self.pending: Dict["Transaction", datetime] = {}  # to add
        self.__inner_lock = Lock()
        self.outer_lock = Lock()
        self.backup_thread = Thread(target=self.backup_cleaner, daemon=True)
        self.backup_thread.start()

    def add_amount(self, transaction: "Transaction", is_commit: bool) -> bool:
        with self.__inner_lock:
            if not is_commit:
                self.pending[transaction] = datetime.now(timezone.utc)
                return True
            else:
                if transaction not in self.pending:
                    raise ExpiredTransaction(
                        "Transaction is either first-seen or expired"
                    )
                else:
                    self.balance += transaction.amount
                    del self.pending[transaction]
                    return True

    def withhold_amount(self, transaction: "Transaction", is_commit: bool) -> bool:
        with self.__inner_lock:
            if self.balance > transaction.amount:
                if is_commit:
                    if transaction in self.frozen:
                        del self.frozen[transaction]
                        return True
                    else:
                        raise ExpiredTransaction(
                            "Transaction is either first-seen or expired"
                        )
                else:
                    self.balance -= transaction.amount
                    self.frozen[transaction] = datetime.now(timezone.utc)
                    return True
            else:
                raise AmountExceedsBalance(
                    f"Requested sum {transaction.amount} exceeds balance"
                )  # we do not reveal the exact amount

    def backup_cleaner(
        self,
    ):  # in a backend threat will clean log upon timeout and mark transaction as failed
        while True:
            with self.__inner_lock:
                now = datetime.now(timezone.utc)
                frozen_copy = self.frozen.copy()
                for transaction, ts in frozen_copy.items():
                    if (now - ts).total_seconds() > GLOBAL_TIMEOUT:
                        self.balance += transaction.amount
                        del self.frozen[transaction]
                pending_copy = self.pending.copy()
                for transaction, ts in pending_copy.items():
                    if (now - ts).total_seconds() > GLOBAL_TIMEOUT:
                        if transaction.state == TransactionState.COMPLETED:
                            self.balance += transaction.amount
                            del self.pending[transaction]
                        else:
                            del self.pending[transaction]
            time.sleep(60)


class User:
    def __init__(self, name: str, dob: datetime):
        self.name = name
        self.dob = dob
        self.open_accounts: List[Account] = []
        self.closed_accounts: list[Account] = []

    def open_account(self, starting_balance: int) -> None:
        new_account = Account(starting_balance, self)
        self.open_accounts.append(new_account)

    def close_account(self, account: Account) -> None:
        if account in self.open_accounts:
            self.open_accounts.pop(self.open_accounts.index(account))
        else:
            raise NoMatchingAccount("This user has no matching account")


@dataclass
class Transaction:
    _id_counter: ClassVar[int] = 0
    _id_lock: ClassVar[Lock] = Lock()

    id: int = field(init=False)
    timestamp: datetime = field(init=False)

    sender: Account = field(compare=False)
    receiver: Account = field(compare=False)
    amount: int = field(compare=False)
    state: TransactionState = field(compare=False)

    def __post_init__(self):
        cls = type(self)
        with cls._id_lock:
            cls._id_counter += 1
            self.id = cls._id_counter
        self.timestamp = datetime.now(timezone.utc)

    def __hash__(self):
        return hash(self.id)


class TransactionRepository:
    def __init__(self):
        self.__lock = Lock()
        self.transaction_log: Set[Transaction] = set()

    def append_transaction(self, transaction: Transaction) -> None:
        with self.__lock:
            self.transaction_log.add(transaction)


class StripePaymentProcessor:
    def __init__(self, transaction_log: TransactionRepository):
        self.log = transaction_log

    def send_money(self, sender: Account, receiver: Account, amount: int):
        transaction = Transaction(sender, receiver, amount, TransactionState.NEW)
        # transaction_id = transaction.id
        self.log.append_transaction(transaction)
        with sender.outer_lock, receiver.outer_lock:
            transaction.state = TransactionState.IN_PROGRESS
            try:
                sender.withhold_amount(transaction, is_commit=False)
            except AmountExceedsBalance:
                transaction.state = TransactionState.FAILED
                raise AmountExceedsBalance("Sender balance is below requested amount")

            try:
                receiver.add_amount(transaction, is_commit=False)
            except:
                transaction.state = TransactionState.FAILED
                raise FailedTransaction("Receiver failed to receive")
                # we do nothing beyond it, because it will auto-expiry at sender side

            try:
                sender.withhold_amount(transaction, is_commit=True)
                transaction.state = TransactionState.COMPLETED
            except ExpiredTransaction:
                transaction.state = TransactionState.FAILED
                raise FailedTransaction("Transaction time'd out")
                # we do nothing beyond as it will auto-expiry at the receiver side

            try:
                receiver.add_amount(transaction, is_commit=True)
            except ExpiredTransaction:
                if transaction.state == TransactionState.COMPLETED:
                    return  # we are positive as eventual cleaner will do the job
                else:
                    transaction.state = TransactionState.FAILED
                    # edge case and we need a special manager for it
                    raise CriticalError(
                        "CRITICAL ERROR: SENDER BALANCE IS UPDATED BUT RECEIVER SEEMS TO BE NOT"
                    )


class LedgerSystem:
    def __init__(self):
        self.transaction_log = TransactionRepository()
        self.payment_processor: StripePaymentProcessor = StripePaymentProcessor(
            self.transaction_log
        )

    def add_user(self, name: str, dob: datetime): ...  # interface to add users

    def open_account(self, balance: int, user: User): ...  # interface to open accounts

    def close_account(self, account: Account): ...  # interface to close accounts

    def send_money(self, sender: Account, receiver: Account, amount: int):
        try:
            self.payment_processor.send_money(sender, receiver, amount)
        except FailedTransaction:
            raise FailedTransaction("Failed to process payment")
