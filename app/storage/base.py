from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

class Item(BaseModel):
    """Represents a file or a folder."""
    name: str
    path: str
    type: str  # 'file' or 'folder'

class StorageBackend(ABC):
    """Abstract Base Class for all storage backends."""

    @abstractmethod
    def list(self, path: str) -> List[Item]:
        """Lists files and folders at a given path."""
        pass