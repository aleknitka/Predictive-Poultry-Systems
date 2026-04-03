from pydantic import BaseModel
from enum import StrEnum

class CustomerSegmentTypes(StrEnum):
    GENERATION_A = "Generation A"
    GENERATION_Z = "Generation Z"
    MILENNIALS = "Milennials"
    GENERATION_X = "Generation X"
    BOOMERS = "Boomers"

class CustomerSegment(BaseModel):
    name: CustomerSegmentTypes
    profile: str
    preferences: str