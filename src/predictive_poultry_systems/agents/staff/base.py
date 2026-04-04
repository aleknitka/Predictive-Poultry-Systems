"""Primitive objects for store staff"""

from typing import Annotated, Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum
from predictive_poultry_systems.agents.behavior.bt.base import Node
from predictive_poultry_systems.agents.behavior.llm.agents import DecisionAgent


class StaffRoles(StrEnum):
    CASHIER = "cashier"
    FRY_COOK = "fry_cook"
    GRILL_MASTER = "grill_master"
    MANAGER = "manager"
    CLEANER = "cleaner"
    RUNNER = "runner"


class BaseStaff(BaseModel):
    """
    Base staff object representing an employee in the fulfillment node.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    role: StaffRoles
    hourly_wage: Annotated[float, Field(ge=0.0, description="cost per hour of labor")]
    skill_level: Annotated[
        float, Field(ge=0.0, le=1.0, description="skill level (1.0 = 100% efficient)")
    ]
    fatigue_rate: Annotated[
        float, Field(ge=0.0, description="rate at which fatigue increases per timestep")
    ]
    shift_hours: Annotated[
        float, Field(ge=0.0, description="standard shift duration in hours")
    ]

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
    efficiency_modifier: float = Field(
        default=1.0, description="Current efficiency multiplier"
    )
