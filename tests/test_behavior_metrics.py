import math
from predictive_poultry_systems.agents.behavior.metrics import (
    calculate_crisp_state,
    update_satisfaction,
    calculate_morale,
)


def test_calculate_crisp_state():
    # mu = 240, sigma = 20
    assert calculate_crisp_state(240) == 1.0

    # 1 sigma away (220 or 260) -> exp(-0.5) ~ 0.606
    assert math.isclose(calculate_crisp_state(220), math.exp(-0.5), rel_tol=1e-5)
    assert math.isclose(calculate_crisp_state(260), math.exp(-0.5), rel_tol=1e-5)

    # Far away (180 or 300) -> exp(-((60)**2)/(2*400)) = exp(-3600/800) = exp(-4.5) ~ 0.011
    assert calculate_crisp_state(180) < 0.02
    assert calculate_crisp_state(300) < 0.02


def test_update_satisfaction():
    # expected_sos = 180, base = 10.0, k = 0.005
    # At or below threshold, no decay
    assert update_satisfaction(180) == 10.0
    assert update_satisfaction(150) == 10.0

    # After threshold: 300s -> 120s decay -> 10 * exp(-0.005 * 120) = 10 * exp(-0.6) ~ 5.488
    expected = 10.0 * math.exp(-0.005 * 120)
    assert math.isclose(update_satisfaction(300), expected, rel_tol=1e-5)


def test_calculate_morale():
    # Morale = 10.0 * (1.0 - fatigue) * skill_level
    assert calculate_morale(0.0, 1.0) == 10.0
    assert calculate_morale(0.0, 0.5) == 5.0
    assert calculate_morale(0.5, 1.0) == 5.0

    # 0.5 fatigue and 0.5 skill -> 10 * 0.5 * 0.5 = 2.5
    assert calculate_morale(0.5, 0.5) == 2.5

    # Full fatigue -> 0 morale
    assert calculate_morale(1.0, 1.0) == 0.0
