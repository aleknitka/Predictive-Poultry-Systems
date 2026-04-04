from typing import List, Any
from pydantic import Field
from .base import Node, Status


class Composite(Node):
    """Base class for nodes with children."""

    children: List[Node] = Field(default_factory=list)
    last_running_index: int = Field(default=0, exclude=True)


class Sequence(Composite):
    """
    Ticks children one by one.
    Returns SUCCESS if all children succeed.
    Returns FAILURE if any child fails.
    Returns RUNNING if a child returns RUNNING.
    """

    def tick(self, context: Any) -> Status:
        for i in range(self.last_running_index, len(self.children)):
            child = self.children[i]
            status = child.tick(context)

            if status == Status.RUNNING:
                self.last_running_index = i
                return Status.RUNNING

            if status == Status.FAILURE:
                self.last_running_index = 0
                return Status.FAILURE

        self.last_running_index = 0
        return Status.SUCCESS


class Selector(Composite):
    """
    Ticks children one by one.
    Returns SUCCESS if any child succeeds.
    Returns FAILURE if all children fail.
    Returns RUNNING if a child returns RUNNING.
    """

    def tick(self, context: Any) -> Status:
        for i in range(self.last_running_index, len(self.children)):
            child = self.children[i]
            status = child.tick(context)

            if status == Status.RUNNING:
                self.last_running_index = i
                return Status.RUNNING

            if status == Status.SUCCESS:
                self.last_running_index = 0
                return Status.SUCCESS

        self.last_running_index = 0
        return Status.FAILURE
