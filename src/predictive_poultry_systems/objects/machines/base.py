"""Primitive objects for store machines"""

from typing import Annotated
from pydantic import BaseModel, Field, model_validator
from enum import StrEnum
from predictive_poultry_systems.objects.menu.base import MenuItemTypes, IngredientTypes


class MachineTypes(StrEnum):
    # Thermal
    COOKING = "cooking"
    HEATING = "heating"  # holding/warming lamps
    REFRIGERATION = "refrigeration"
    # Product flow
    STORAGE = "storage"
    PREPARATION = "preparation"
    PACKAGING = "packaging"
    DISPENSING = "dispensing"  # drinks, sauces
    CONVEYOR = "conveyor"
    # Customer interface
    ORDERING = "ordering"  # kiosk / till
    PAYMENT = "payment"
    # Facility
    CLEANING = "cleaning"
    VENTILATION = "ventilation"


class MachineWasteTypes(StrEnum):
    """
    Machines produce waste
    """

    ORGANIC = "organic"
    RECYCLABLE = "recyclable"
    NONRECYCLABLE = "non-recyclable"


class MachineConsumptionTypes(StrEnum):
    """
    Different resource types that a given machine can consume, non-food things
    """

    FTE = "fte"
    POWER = "pwr"
    WATER = "h2o"
    GAS = "gas"


class OperationModes(BaseModel):
    """
    Standard operation modes for the machinery, each mode consumes energy/resources
    """

    idle: Annotated[
        float, Field(ge=0.0, description="consumption per timestep when idle.")
    ]
    working: Annotated[
        float, Field(ge=0.0, description="consumption per timestep when working.")
    ]
    off: Annotated[
        float,
        Field(
            ge=0.0, description="consumption, if any per timestep when machine is off."
        ),
    ]
    faulted: Annotated[
        float,
        Field(
            ge=0.0,
            description="consumption per timestep when machine is faulted (e.g., cooling still runs).",
        ),
    ]


class BaseMachine(BaseModel):
    """
    Base machine object class representing a physical asset in the node.
    """

    name: str
    icon: str
    type: MachineTypes
    corporate_name: str

    # Resource Consumption
    inputs: dict[MachineConsumptionTypes, OperationModes]

    # Material Transformation
    ingredient_inputs: dict[IngredientTypes, float] = Field(
        default_factory=dict, description="ingredients consumed per production cycle"
    )
    outputs: dict[
        MenuItemTypes,
        Annotated[
            float, Field(ge=0.0, description="units produced per production cycle")
        ],
    ]

    # Waste Modeling
    waste_outputs: dict[MachineWasteTypes, float] = Field(
        default_factory=dict, description="waste produced per production cycle"
    )
    waste_disposal_costs: dict[MachineWasteTypes, float] = Field(
        default_factory=dict, description="cost per standardized unit of waste disposal"
    )

    # Reliability
    fault_rate: Annotated[
        float,
        Field(
            ge=0.0,
            le=1.0,
            description="probability of fault per production cycle or timestep",
        ),
    ]
    repair_time_mean: Annotated[
        float, Field(ge=0.0, description="mean time to repair in timesteps")
    ]

    @model_validator(mode="after")
    def validate_reliability(self) -> "BaseMachine":
        if self.fault_rate > 0 and self.repair_time_mean <= 0:
            raise ValueError(
                "Machines with a non-zero fault rate must have a non-zero repair_time_mean"
            )
        return self
