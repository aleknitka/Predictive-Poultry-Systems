"""Primitive objects for store staff"""

from typing import Annotated
from pydantic import BaseModel, Field
from enum import StrEnum


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
