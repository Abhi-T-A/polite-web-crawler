from abc import ABC, abstractmethod
from typing import List
from app.models.record import BookRecord


class Storage(ABC):
    """
    Abstract base class establishing the contract for all storage backends.
    """

    @abstractmethod
    def save(self, records: List[BookRecord]) -> None:
        """
        Persist a list of BookRecord objects into the underlying storage medium.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Clean up resources, close file handles or database connections.
        """
        pass
