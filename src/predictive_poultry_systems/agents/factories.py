import random
from faker import Faker
from .customers.base import BaseCustomer
from .staff.base import BaseStaff, StaffRoles
from .customers.segments import CustomerSegment, CustomerSegmentTypes
from .customers.loyalty import CustomerLoyalty, CustomerLoyaltyLevel
from .customers.rfm import CustomerRFMProfile
from .customers.behavior import get_default_customer_tree
from .staff.behavior import get_default_staff_tree

fake = Faker()


def create_customer_data() -> BaseCustomer:
    """Generates varied customer data using Faker."""
    segment_type = random.choice(list(CustomerSegmentTypes))
    loyalty_level = random.choice(list(CustomerLoyaltyLevel))

    return BaseCustomer(
        segment=CustomerSegment(
            name=segment_type,
            profile=fake.paragraph(nb_sentences=1),
            preferences=fake.word(),
        ),
        satisfaction=random.uniform(3.0, 9.0),
        price_sensitivity=random.uniform(0.1, 0.9),
        promo_sensitivity=random.uniform(0.1, 0.9),
        loyalty=CustomerLoyalty(
            level=loyalty_level,
            rfm=CustomerRFMProfile(
                recency=random.randint(1, 5),
                frequency=random.randint(1, 5),
                monetary=random.randint(1, 5),
            ),
        ),
        root_node=get_default_customer_tree(),
    )


def create_staff_data(
    name: str = None, role: StaffRoles = StaffRoles.FRY_COOK
) -> BaseStaff:
    """Generates varied staff data."""
    return BaseStaff(
        name=name or fake.name(),
        role=role,
        hourly_wage=random.uniform(15.0, 25.0),
        skill_level=random.uniform(0.7, 1.0),
        fatigue_rate=random.uniform(0.005, 0.02),
        shift_hours=8.0,
        root_node=get_default_staff_tree(),
    )
