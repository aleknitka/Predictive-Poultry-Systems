"""Primitive objects for store facilities"""

from typing import Annotated
from pydantic import BaseModel, Field
from enum import StrEnum


class FacilityTypes(StrEnum):
    CHAIR = "chair"
    TABLE = "table"
    TOILET = "toilet"
    QUEUE_AREA = "queue_area"
    KITCHEN_ZONE = "kitchen_zone"
    STORAGE_ZONE = "storage_zone"
    PARKING_SPOT = "parking_spot"


class BaseFacility(BaseModel):
    """
    Base facility object representing a physical space or utility in the node.
    """

    name: str
    type: FacilityTypes
    capacity: Annotated[
        int,
        Field(ge=1, description="maximum number of units (people/assets) it can hold"),
    ]
    occupied: Annotated[
        int, Field(ge=0, description="current number of occupied units")
    ]

    @property
    def available_capacity(self) -> int:
        return self.capacity - self.occupied


class StoreLayout(BaseModel):
    """
    Aggregates all facilities and zones within a fulfillment node.
    """

    node_id: str
    total_area_sqm: Annotated[float, Field(ge=0.0)]
    facilities: list[BaseFacility] = Field(default_factory=list)
