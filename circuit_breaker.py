import random
from typing import Any, Tuple
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum
from threading import Lock, Thread

@dataclass
class Limit:
	count: int # amount of failures
	time: int # time in which failures occur – we do a sliding window, aren't we?


class CircuitBreakerState(Enum):
	OPEN = 1
	HALF_OPEN = 2
	CLOSED = 3


class CircuitBreaker(ABC):
	@abstractmethod
	def breaker(self, func):
		return func


class CircuitBreakerBoolean(CircuitBreaker):
	def __init__(self, timeout_in_secs: int, limit: Limit):
		assert (limit is Limit), "value must be Limit class"
		self.__timeout = timeout_in_secs
		self.failed_attempts = []
		self.__limit = limit
		self.state = CircuitBreakerState.CLOSED # all reqs are passed by defaul unless specified otherwise
		self.__flipper = True
		self.__lock = Lock()
		self.__run_clean_log = Thread(target=clean_log, daemon=True)
		self.__run_set_state = Thread(target=set_state, daemon=True)
		self.__run_clean_log.start()
		self.__run_set_state.start()
		
	@property
	def timeout(self):
		return self.__timeout
		
	@timeout.setter
	def timeout(self, value):
		self.__timeout = value
		
	@property
	def limit(self):
		return self.__limit
	
	@limit.setter
	def limit(self, value):
		assert (value is Limit), "value must be Limit class"
		self.__limit = value
		
	@property
	def failure_counter(self):
		return len(self.failed_attempts)
	
	def breaker(self, func):
		def decorator(func):
			def wrapper(caller_self, *args, **kwargs):
				if self.state == CircuitBreakerState.OPEN or CircuitBreakerState.HALF_OPEN and self.__flipper:
					res = func(caller_self, *args, **kwargs)
					if res is False:
						self.failed_attempts.append(datetime.now(timezone.utc))
					self.__flipper = False
					return res
				elif CircuitBreakerState.HALF_OPEN and not self.__flipper:
					self.__flipper = True
				else:
					print("Timeout period")
					return False
			return wrapper
		return decorator
		
	def clean_log(self):
		while True:
			counter = -1
			now = datetime.now(timezone.utc)
			for row in self.failed_attempts:
				if (row-now).total_seconds() > self.limit.time:
					counter += 1
			if counter >= 0:
				with self.__lock:
					self.failed_attempts = self.failed_attempts[counter:]
				
	def set_state(self):
		while True:
			if self.state == CircuitBreakerState.CLOSED:
				if self.failure_counter > self.limit.count:
					self.state = CircuitBreakerState.OPEN
			elif self.state == CircuitBreakerState.HALF_OPEN:
				now = datetime.now(timezone.utc)
				time.sleep(self.timeout//2)
				counter = 0
				with self.__lock:
					for row in reversed(self.failed_attempts):
						if row < now:
							counter += 1
						else:
							break
				if counter > self.limit.count // 4:  #let's say we keep gates close until the system cooldowns to at least 50% of acceptable errors
					self.state = CircuitBreakerState.OPEN
				else:
					self.state = CircuitBreakerState.CLOSED
			else:
				time.sleep(self.timeout)
				self.state = CircuitBreakerState.HALF_OPEN 


current_limit = Limit(count=100, time=60) # 100 failures in 60 seconds
circuit_breaker = CircuitBreakerBoolean(timeout_in_secs=120, limit=current_limit)

class SomeBackendService:
	def __init__(self, failure_ratio: int) -> None:
		self.__failure_ratio = failure_ratio
	
	@property
	def failure_ratio(self) -> int:
		return self.__failure_ratio
	
	@failure_ratio.setter
	def failure_ratio(self, value):
		self.__failure_ratio = value
	
	def mock_call(self) -> bool:
		i = random.randint(0, 100)
		if i <= self.failure_ratio:
			return False
		else:
			return True
		

class SomeCaller:
	def __init__(self, backend_service: SomeBackendService):
		self.backend_service = backend_service
	
	@circuit_breaker.breaker
	def call_backend(self):
		res = self.backend_service.mock_call()
		return res
		
if __name__ == "__main__":
	backend_service = SomeBackendService(80) #fails 80% of time
	caller = SomeCaller(backend_service)
		