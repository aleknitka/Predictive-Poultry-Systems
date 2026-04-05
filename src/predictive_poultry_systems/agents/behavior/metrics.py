import math
from predictive_poultry_systems.config import EXPECTED_SOS_MINUTES


def calculate_crisp_state(
    cook_time: float, mu: float = 240.0, sigma: float = 20.0
) -> float:
    """
    Evaluates how close a cooked asset is to its thermodynamic optimum using a Gaussian scoring function.

    Args:
        cook_time: Actual time spent cooking in seconds.
        mu: Optimal cook time (peak of the Gaussian).
        sigma: Standard deviation (width of the optimal window).

    Returns:
        A score between 0.0 and 1.0.
    """
    return math.exp(-((cook_time - mu) ** 2) / (2 * sigma**2))


def update_satisfaction(
    wait_time: float,
    base_satisfaction: float = 10.0,
    expected_sos: float = EXPECTED_SOS_MINUTES,
    k: float = 0.005,
) -> float:
    """
    Calculates customer satisfaction decay based on wait time (Speed of Service).

    Formula: base_satisfaction * exp(-k * max(0, wait_time - expected_sos))
    """
    decay_time = max(0.0, wait_time - expected_sos)
    return base_satisfaction * math.exp(-k * decay_time)


def calculate_morale(fatigue: float, skill_level: float) -> float:
    """
    Calculates staff morale based on fatigue and skill level.

    Args:
        fatigue: Current fatigue level (0.0 to 1.0).
        skill_level: Skill level (0.0 to 1.0).

    Returns:
        Morale score between 0.0 and 10.0.
    """
    # Morale = 10.0 * (1.0 - fatigue) * skill_level
    return 10.0 * (1.0 - fatigue) * skill_level
