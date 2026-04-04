from typing import Any, Type, TypeVar, Optional
from pydantic import BaseModel
from pydantic_ai import Agent
from .providers import get_model

T = TypeVar("T", bound=BaseModel)


class DecisionAgent:
    """Wrapper around pydantic-ai.Agent for common decision patterns."""

    def __init__(
        self, result_type: Type[T], system_prompt: str, model_id: Optional[str] = None
    ):
        self.model = get_model(model_id)
        self.agent = Agent(
            model=self.model, output_type=result_type, system_prompt=system_prompt
        )

    async def decide(self, user_prompt: str, deps: Any = None) -> T:
        """Run the agent and return the structured result."""
        result = await self.agent.run(user_prompt, deps=deps)
        return result.output
