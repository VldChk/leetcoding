from abc import ABC, abstractmethod
from typing import List, Dict
from threading import Thread, Lock
from queue import Queue
import time
from dataclasses import dataclass

# from __future__ import annotations


class CapacityExceeds(Exception):
    pass


class NoRunningServer(Exception):
    pass


@dataclass
class ServerAddress:
    host: str
    port: int


# Server


class Server:
    def __init__(
        self, address: ServerAddress
    ) -> None:  # replace str -> Address for the future
        self.address = address
        self.load = 0
        self.capacity = 1
        self.requests_queue = Queue()
        self.request_processor = Thread(target=self.process_requests, daemon=True)
        self.request_processor.start()
        self._load_lock = Lock()
        self.heartbeat_queue = Queue()
        self.heartbeat_pulsar = Thread(target=self.send_heartbeat, daemon=True)
        self.heartbeat_pulsar.start()

    def submit_request(self, request: Dict[str, str]) -> None:
        with self._load_lock:
            self.load += 1
            self.requests_queue.put(request)

    def process_requests(self) -> None:
        while True:
            request = self.requests_queue.get()
            with self._load_lock:
                # emulating the processing
                time.sleep(5)
                self.load = max(
                    self.load - 1, 0
                )  # just in case we process duplicates and get below zero

    def send_heartbeat(self) -> None:
        """
        This is just an emulation to showcase the logic
        In real life the queue will be outside of the Server, because then it will not be accessible
        """
        while True:
            self.heartbeat_queue.put(True)
            n = len(self.heartbeat_queue.queue)
            for i in range(3, n):
                self.heartbeat_queue.get()
            time.sleep(
                3
            )  # we ping every 3 seconds but make sure no more that 3 messages are queued to avoid overflow


# Balance Strategies


class LoadBalancerStrategy(ABC):

    @abstractmethod
    def select_server(self, servers: List[Server]) -> Server:
        pass


class RoundRobinBalanceStrategy(LoadBalancerStrategy):
    def __init__(self):
        self.counter = 0
        self._lock = Lock()

    def select_server(self, servers: List[Server]) -> Server:
        with self._lock:
            n = len(servers)
            if n == 0:
                raise NoRunningServer("No server is running")
            idx = self.counter % n
            self.counter += 1
            return servers[idx]


# Main class


class LoadBalancer:
    def __init__(self, max_capacity: int) -> None:
        self.max_capacity: int = max_capacity
        self.servers: List[Server] = (
            []
        )  # potentially dictionary if we want to store more info, like last timestamp, etc.
        self.balancer = RoundRobinBalanceStrategy()
        self.inactive_servers: List[Server] = []
        self._add_server_lock = Lock()

    @property
    def num_of_servers(self) -> int:
        return len(self.servers)

    def add_server(self, server: Server) -> None:
        """
        In this exercise we assume that server management is beyond the scope of LoadBalancer
        """
        with self._add_server_lock:
            if self.num_of_servers < self.max_capacity:
                self.servers.append(server)
            else:
                raise CapacityExceeds(
                    f"Can't add a new server due to exceeds of capacity: {self.max_capacity}"
                )

    def remove_server(self, server: Server) -> None:
        """
        Similar to add_server, we presume that responsibility to shutdown server
        is beyond the scope of LoadBalancer
        """
        self.servers.pop(self.servers.index(server))

    def change_capacity(self, max_capacity: int) -> None:
        self.max_capacity = max_capacity

    def heartbeat(self) -> None:
        """
        This is just an emulation to showcase the logic
        """
        while True:
            for server in self.servers:
                heartbeat = server.heartbeat_queue.get()
                if not heartbeat:
                    self.servers.pop(
                        self.servers.index(server)
                    )  # not sure though we can remove item from the list during runtime
                    self.inactive_servers.append(server)
            for server in self.inactive_servers:
                if self.num_of_servers >= self.max_capacity:
                    continue
                else:
                    heartbeat = server.heartbeat_queue.get()
                    if heartbeat:
                        with self._add_server_lock:
                            self.servers.append(server)
                            self.inactive_servers.pop(
                                self.inactive_servers.index(server)
                            )
            # by this we make sure that our cycle is 100% longer than hearbeat sends from the server
            time.sleep(3)

    def direct_request(self, request: Dict[str, str]) -> None:
        if self.num_of_servers > 0:
            try:
                elected_server = self.balancer.select_server(self.servers)
                elected_server.submit_request(request)
            except NoRunningServer:
                raise NoRunningServer("No server is running")
        else:
            """
            Here we have two architectural choices:
            - We can just throw an error and tell to client to add servers
            - Or we can "park" request into the queue and wait for new server added

            Here we throw an error but later can switch or add an optional flag
            """
            raise NoRunningServer("No server is running")
