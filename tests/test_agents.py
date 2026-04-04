from predictive_poultry_systems.agents.customers.rfm import CustomerRFMProfile
import pytest
from pydantic import ValidationError


def test_rfm_profile_creation():
    profile = CustomerRFMProfile(recency=5, frequency=3, monetary=1)
    assert profile.recency == 5
    assert profile.frequency == 3
    assert profile.monetary == 1


def test_rfm_profile_validation():
    # Valid data
    profile = CustomerRFMProfile(recency=0, frequency=5, monetary=5)
    assert profile.monetary == 5

    # Invalid data: recency > 5.0
    with pytest.raises(ValidationError):
        CustomerRFMProfile(recency=6, frequency=1, monetary=1)

    # Invalid data: frequency < 0.0
    with pytest.raises(ValidationError):
        CustomerRFMProfile(recency=1, frequency=-1, monetary=1)
