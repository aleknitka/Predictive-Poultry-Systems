from typing import Annotated
from pydantic import BaseModel, Field


class CustomerRFMProfile(BaseModel):
    recency = Annotated[
        int, Field(ge=0.0, le=5.0, description="Time since the last purchase")
    ]
    frequency = Annotated[
        int,
        Field(ge=0.0, le=5.0, description="Total number of purchases in a set period"),
    ]
    monetary = Annotated[int, Field(ge=0.0, le=5.0, description="Total Spend")]
