from typing import Any, Callable
from .base import Node, Status


class ActionNode(Node):
    """Base class for action nodes."""

    pass


class ConditionNode(Node):
    """Base class for condition nodes."""

    pass


class LambdaAction(ActionNode):
    """An action node that executes a callable."""

    # We use Optional[Callable] to support Pydantic model validation
    # though it will be passed at runtime usually.
    # In practice, for a Digital Twin, we'd probably have specific
    # Action subclasses instead of lambdas for better serialization.
    func: Callable[[Any], Status]

    def tick(self, context: Any) -> Status:
        return self.func(context)


class LambdaCondition(ConditionNode):
    """A condition node that evaluates a callable."""

    func: Callable[[Any], bool]

    def tick(self, context: Any) -> Status:
        return Status.SUCCESS if self.func(context) else Status.FAILURE
