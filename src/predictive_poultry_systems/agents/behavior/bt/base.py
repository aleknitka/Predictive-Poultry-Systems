from enum import Enum
from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, ConfigDict


class Status(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class Node(BaseModel, ABC):
    """Base class for all Behavior Tree nodes."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str

    @abstractmethod
    def tick(self, context: Any) -> Status:
        """Evaluate the node and return its status."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}'>"
