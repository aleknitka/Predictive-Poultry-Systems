from enum import StrEnum

from pydantic import BaseModel

from predictive_poultry_systems.agents.customers.rfm import CustomerRFMProfile


class CustomerLoyaltyLevel(StrEnum):
	HIBERNATING = "Hibernating"
	AT_RISK = "At risk"
	POTENTIAL_LOYAL = "Potential loyal"
	LOYAL = "Loyal"
	CHAMPION = "Champion"
	HARDCORE = "Hardcore"


class CustomerLoyalty(BaseModel):
	level: CustomerLoyaltyLevel
	rfm: CustomerRFMProfile
