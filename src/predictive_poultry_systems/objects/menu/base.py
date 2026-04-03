from enum import Enum, StrEnum
from typing import Annotated

from pydantic import BaseModel, Field


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
	PACKAGING = "packaging"


class MenuItemTypes(StrEnum):
	FRIED_CHICKEN_WHOLE = "whole fried chicken"
	FRIED_CHICKEN_WING = "fried chicken wing"
	FRIED_CHICKEN_LEG = "friend chicken leg"


class BaseMenuItem(BaseModel):
	"""
	Base class for all menu items
	"""

	type: MenuItemTypes
	size: MenuItemSizes
	name: str
	icon: str
	wholesale_price: Annotated[float, Field(description="retailer price per unit")]
	manu_price: Annotated[float, Field(description="customer price per unit")]
	ingredients: dict[
		IngredientTypes, float
	]  # qty in standardised units per item produced
	waste: Annotated[
		float, Field(description="waste in standardised units per item produced")
	]
	corporate_name: str
