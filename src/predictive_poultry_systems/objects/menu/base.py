from typing import Annotated
from pydantic import BaseModel, Field, model_validator
from enum import Enum, StrEnum


class MenuItemSizes(Enum):
    """
    Multiplicators indicating size of an menu item
    """

    SMALL = 0.7
    REGULAR = 1.0
    LARGE = 1.2


class IngredientTypes(StrEnum):
    CHICKEN_WHOLE = "chicken_whole"
    CHICKEN_BREAST = "chicken_breast"
    CHICKEN_WING = "chicken_wing"
    CHICKEN_THIGH = "chicken_thigh"
    BREADING = "breading"
    OIL = "oil"
    SEASONING = "seasoning"
    POTATOES = "potatoes"
    FROZEN_FRIES = "frozen_fries"
    BURGER_BUNS = "burger_buns"
    RAW_PATTIES = "raw_patties"
    LETTUCE = "lettuce"
    SODA_SYRUP = "soda_syrup"
    WATER = "water"


class PackagingTypes(StrEnum):
    BOX = "box"
    CUP = "cup"
    BAG = "bag"
    WRAPPER = "wrapper"


class MenuItemTypes(StrEnum):
    FRIED_CHICKEN_WHOLE = "whole fried chicken"
    FRIED_CHICKEN_WING = "fried chicken wing"
    FRIED_CHICKEN_LEG = "friend chicken leg"
    FRIES = "fries"
    SODA = "soda"
    BURGER = "burger"
    COMBO_MEAL = "combo meal"


class BaseMenuItem(BaseModel):
    """
    Base class for all menu items
    """

    type: MenuItemTypes
    size: MenuItemSizes
    name: str
    icon: str
    wholesale_price: Annotated[
        float, Field(ge=0.0, description="retailer price per unit")
    ]
    manu_price: Annotated[float, Field(ge=0.0, description="customer price per unit")]
    ingredients: dict[
        IngredientTypes, float
    ]  # qty in standardised units per item produced
    packaging: dict[PackagingTypes, int] = Field(
        default_factory=dict, description="required packaging per item"
    )
    waste: Annotated[
        float,
        Field(ge=0.0, description="waste in standardised units per item produced"),
    ]
    corporate_name: str


class ComboMeal(BaseModel):
    """
    Aggregates multiple BaseMenuItem instances into a single customer-facing product
    """

    name: str
    icon: str
    type: MenuItemTypes = MenuItemTypes.COMBO_MEAL
    items: list[BaseMenuItem] = Field(
        min_length=2, description="A combo meal must contain at least 2 items"
    )
    manu_price: Annotated[
        float, Field(ge=0.0, description="Bundled customer price for the combo")
    ]
    combo_packaging: dict[PackagingTypes, int] = Field(
        default_factory=dict, description="Packaging specifically for the combo"
    )

    @model_validator(mode="after")
    def validate_combo_price(self) -> "ComboMeal":
        total_individual_price = sum(item.manu_price for item in self.items)
        if self.manu_price > total_individual_price:
            raise ValueError(
                "Combo price cannot exceed the sum of individual item prices"
            )
        return self
