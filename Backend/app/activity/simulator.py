import random
import time

from app.models.schemas import ActivitySnapshot


SCENARIOS = [
    "FOCUSED",
    "NORMAL",
    "COGNITIVE_LOAD",
    "FATIGUED",
    "LOW_ENGAGEMENT",
]


def get_current_scenario() -> str:
    """
    Development-only controlled scenario cycle.

    Each scenario lasts five seconds.
    """

    index = int(time.time() / 5) % len(SCENARIOS)

    return SCENARIOS[index]


def generate_activity_snapshot() -> ActivitySnapshot:
    scenario = get_current_scenario()

    if scenario == "FOCUSED":
        effort = random.uniform(0.55, 0.70)
        fatigue = random.uniform(0.10, 0.25)

    elif scenario == "NORMAL":
        effort = random.uniform(0.45, 0.60)
        fatigue = random.uniform(0.25, 0.40)

    elif scenario == "COGNITIVE_LOAD":
        effort = random.uniform(0.75, 0.90)
        fatigue = random.uniform(0.35, 0.55)

    elif scenario == "FATIGUED":
        effort = random.uniform(0.75, 0.95)
        fatigue = random.uniform(0.80, 0.98)

    else:
        # LOW_ENGAGEMENT
        effort = random.uniform(0.15, 0.30)
        fatigue = random.uniform(0.05, 0.20)

    heart_rate = (
        75.0
        + effort * 105.0
        + random.uniform(-4.0, 4.0)
    )

    speed = (
        5.5
        + effort * 8.0
        + random.uniform(-0.3, 0.3)
    )

    return ActivitySnapshot(
        activity="running",
        scenario=scenario,
        heart_rate_bpm=round(
            heart_rate,
            1,
        ),
        speed_kmh=round(
            speed,
            2,
        ),
        effort=round(
            effort,
            3,
        ),
        fatigue=round(
            fatigue,
            3,
        ),
    )