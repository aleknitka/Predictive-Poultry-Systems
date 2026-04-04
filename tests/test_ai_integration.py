import pytest
from pydantic import BaseModel
from pydantic_ai.models.test import TestModel
from predictive_poultry_systems.agents.behavior.llm.agents import DecisionAgent
from predictive_poultry_systems.agents.behavior.llm.providers import get_model


class MyResponse(BaseModel):
    choice: str
    reason: str


@pytest.mark.anyio
async def test_decision_agent():
    # Setup agent with a TestModel that returns specific data
    mock_data = {"choice": "Nuggets", "reason": "They are crisp"}
    test_model = TestModel(custom_output_args=mock_data)

    system_prompt = "You are a poultry expert."

    agent_wrapper = DecisionAgent(
        result_type=MyResponse, system_prompt=system_prompt, model_id="openai:gpt-4o"
    )

    # Use override context manager or manually set model
    with agent_wrapper.agent.override(model=test_model):
        result = await agent_wrapper.decide("What should I eat?")

        assert result.choice == "Nuggets"
        assert result.reason == "They are crisp"


def test_get_model():
    # Verify that get_model returns the correct model type based on prefix
    model = get_model("ollama:llama3")
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    assert isinstance(model, OpenAIChatModel)
    assert isinstance(model._provider, OpenAIProvider)
    assert model._provider.base_url.rstrip("/") == "http://localhost:11434/v1"

    model = get_model("openai:gpt-4")
    assert isinstance(model, OpenAIChatModel)
