"""Primitive objects for operational processes"""

from typing import Annotated
from pydantic import BaseModel, Field
from predictive_poultry_systems.objects.machines.base import MachineTypes
from predictive_poultry_systems.objects.menu.base import IngredientTypes, MenuItemTypes


class ThermodynamicProcess(BaseModel):
    """
    Defines the transformation of ingredients into menu items via thermal or mechanical means.
    """

    name: str
    machine_type: MachineTypes
    ingredient_inputs: dict[IngredientTypes, float] = Field(
        description="Amount of ingredients consumed per process cycle"
    )
    menu_outputs: dict[MenuItemTypes, float] = Field(
        description="Amount of menu items produced per process cycle"
    )
    duration_mean: Annotated[
        float, Field(ge=0.0, description="Mean time in timesteps for transformation")
    ]
    energy_intensity: Annotated[
        float,
        Field(
            ge=0.0, description="Multiplier for energy consumption during this process"
        ),
    ]
    target_temp_c: Annotated[
        float,
        Field(
            description="Target temperature for the avian assets during transformation"
        ),
    ]


class AssemblyProcess(BaseModel):
    """
    Defines the manual steps to combine individual items into meals or final packages.
    """

    name: str
    item_inputs: list[MenuItemTypes] = Field(
        description="List of items required to start assembly"
    )
    output_item: MenuItemTypes = Field(
        description="The resulting assembled item (often COMBO_MEAL)"
    )
    fte_requirement: Annotated[
        float, Field(ge=0.0, description="Number of staff units required for assembly")
    ]
    duration_mean: Annotated[
        float, Field(ge=0.0, description="Mean time in timesteps to assemble")
    ]
