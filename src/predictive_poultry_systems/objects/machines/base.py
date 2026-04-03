"""Primitive objects for store machines"""

from typing import Annotated
from pydantic import BaseModel, Field
from enum import StrEnum

class MachineTypes(StrEnum):
    # Thermal
    COOKING = 'cooking'
    HEATING = 'heating' # holding/warming lamps
    REFRIGERATION = 'refrigeration'
    # Product flow
    STORAGE = 'storage'
    PREPARATION = 'preparation'
    PACKAGING = 'packaging'
    DISPENSING = 'dispensing' # drinks, sauces
    CONVEYOR = 'conveyor'
    # Customer interface
    ORDERING = 'ordering' # kiosk / till
    PAYMENT = 'payment'
    # Facility
    CLEANING = 'cleaning'
    VENTILATION = 'ventilation'

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
    FTE = 'fte'
    POWER = 'pwr'
    WATER = 'h2o'
    GAS = 'gas'

class OperationModes(BaseModel):
    """
    Standard operation modes for the machinery, each mode consumes energy
    """
    idle: Annotated[float, Field(description="consumption per timestep when idle.")]
    working: Annotated[float, Field(description="consumption per timestep when working.")]
    off: Annotated[float, Field(description="consumption, if any per timestep when machine is off.")]


class BaseMachine(BaseModel):
    """
    Base machine object class
    """
    name: str
    icon: str
    type: MachineTypes
    inputs: dict[ConsumptionTypesPerTimestep, OperationModes]
    outputs: dict[MenuItemTypes, Annotated[float, Field(ge=0.0, description="units produced per timestep when working")]]
    corporate_name: str
    fault_rate: Annotated[float, Field(ge=0.0, le=1.0, description="probability of fault per timestep")]




