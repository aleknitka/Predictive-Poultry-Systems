"""Base customer object"""

from typing import Annotated, Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict
from predictive_poultry_systems.agents.customers.loyalty import CustomerLoyalty
from predictive_poultry_systems.agents.customers.segments import CustomerSegment
from predictive_poultry_systems.agents.behavior.bt.base import Node
from predictive_poultry_systems.agents.behavior.llm.agents import DecisionAgent


class BaseCustomer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    segment: CustomerSegment
    satisfaction: Annotated[
        float, Field(ge=0.0, le=10.0, description="satisfaction level")
    ]
    price_sensitivity: Annotated[
        float, Field(ge=0.0, le=1.0, description="price sensitivity level")
    ]
    promo_sensitivity: Annotated[
        float, Field(ge=0.0, le=1.0, description="promo sensitivity level")
    ]
    loyalty: CustomerLoyalty

    # Behavior & Intelligence
    root_node: Optional[Node] = Field(
        default=None, description="Root of the behavior tree"
    )
    brain: Optional[DecisionAgent] = Field(
        default=None, description="LLM-driven decision agent"
    )
    memory: Dict[str, Any] = Field(
        default_factory=dict, description="Agent short-term memory"
    )
