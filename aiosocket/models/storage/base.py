from typing import Dict, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseStorage(Generic[T]):
    """
    Basic storage class for storing objects with a key
    """

    def __init__(self) -> None:
        self._storage: Dict[str, T] = {}

    def add(self, key: str, value: T) -> None:
        """
        Adds an object to the storage with the specified key

        :param key: Key for the object
        :param value: Object to add
        """

        if key in self._storage:
            raise ValueError(f"Object with key '{key}' already exists.")
        self._storage[key] = value

    def get(self, key: str) -> T:
        """
        Gets an object from the storage by the specified key

        :param key: Key for the object
        :return: Object with the specified key
        """

        if key not in self._storage:
            raise KeyError(f"Object with key '{key}' not found.")
        return self._storage[key]

    def remove(self, key: str) -> None:
        """
        Removes an object from the storage by the specified key

        :param key: Key for the object
        """

        if key not in self._storage:
            raise KeyError(f"Object with key '{key}' not found.")
        del self._storage[key]

    def __contains__(self, key: str) -> bool:
        """
        Checks if the storage contains an object with the specified key

        :param key: Key for the object
        """

        return key in self._storage

    def __len__(self) -> int:
        """Returns the number of objects in the storage"""

        return len(self._storage)
