#!/usr/bin/env python3
"""Cache implementation in Redis with cache
call counts and call history.
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Incrments when a method is called in cache

    Args:
        method: The method being observed

    Returns:
        The method call with required arguments
    """
    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        count_key = method.__qualname__
        self._redis.incr(count_key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores history of inputs and outputs of cache methods when
    called

    Args:
        method: The cache method to be observed

    Returns:
        The method called in the cache
    """
    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        data = str(args[1:])
        self._redis.rpush(input_key, data)

        output = method(self, *args, **kwds)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


class Cache():
    def __init__(self):
        """Initialization function
        """
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> uuid.UUID:
        """Stores a value in the cache

        Args:
            data: The value to be stored

        Returns:
            The key to the stored value in the cache
        """
        random_key: uuid.UUID = uuid.uuid4()
        self._redis.set(str(random_key), data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Gets a value stored in the cache

        Args:
            key: The key to the value in memory
            fn: A transformation function to format data. Defaults to None.

        Returns:
            The value associated passed through the transformation function
        """
        data = self._redis.get(key)
        if fn is not None and data is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Gets a string in the cache

        Args:
            key: The key to string data

        Returns:
            The value associated to key as a string
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Gets an integer in the cache

        Args:
            key: Key to integer value

        Returns:
            The value as an integer
        """
        return self.get(key, int)


def replay(func: Callable) -> None:
    """Shows history anc calls of a method in a cache instance

    Args:
        func: The method
    """
    cache = func.__self__
    func_name = func.__qualname__
    func_inputs_key = func_name + ":inputs"
    func_outputs_key = func_name + ":outputs"

    no_of_calls = cache.get_int(func_name)
    inputs = cache._redis.lrange(func_inputs_key, 0, -1)
    outputs = cache._redis.lrange(func_outputs_key, 0, -1)
    inputs = [item.decode('utf-8') for item in inputs]
    outputs = [item.decode('utf-8') for item in outputs]

    calls = zip(inputs, outputs)
    print(f"{func_name.capitalize()} was called {no_of_calls} times")
    for param, output in calls:
        print(f"{func_name}(*('{param}')) -> {output}")
