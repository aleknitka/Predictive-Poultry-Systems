"""Base customer object"""

from typing import Annotated
from pydantic import BaseModel, Field
from predictive_poultry_systems.agents.customers.loyalty import CustomerLoyalty
from predictive_poultry_systems.agents.customers.segments import CustomerSegment


class BaseCustomer(BaseModel):
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
