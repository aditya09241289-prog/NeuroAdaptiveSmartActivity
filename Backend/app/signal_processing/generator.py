import math
import random
import time

import numpy as np

from app.models.schemas import EEGSnapshot
from app.signal_processing.filters import preprocess_eeg


SCENARIOS = [
    "FOCUSED",
    "NORMAL",
    "COGNITIVE_LOAD",
    "FATIGUED",
    "LOW_ENGAGEMENT",
]


def get_current_scenario() -> str:
    """
    Development-only scenario cycle.

    Each scenario lasts 5 seconds so the EEG and activity
    simulators can exercise the complete adaptive pipeline.
    """
    index = int(time.time() / 5) % len(SCENARIOS)
    return SCENARIOS[index]


def generate_synthetic_eeg_snapshot() -> EEGSnapshot:
    sampling_rate = 250
    sample_count = 250

    time_axis = np.arange(sample_count) / sampling_rate

    scenario = get_current_scenario()

    # ---------------------------------------------------------
    # Scenario-specific EEG characteristics
    # ---------------------------------------------------------

    if scenario == "FOCUSED":
        alpha_amplitude = 16.0
        beta_amplitude = 4.0
        theta_amplitude = 5.0

        alpha_power = random.uniform(0.75, 0.95)
        beta_power = random.uniform(0.20, 0.40)
        theta_power = random.uniform(0.20, 0.35)

        artifact_level = random.uniform(0.03, 0.10)

    elif scenario == "NORMAL":
        alpha_amplitude = 10.0
        beta_amplitude = 8.0
        theta_amplitude = 6.0

        alpha_power = random.uniform(0.45, 0.65)
        beta_power = random.uniform(0.40, 0.60)
        theta_power = random.uniform(0.35, 0.50)

        artifact_level = random.uniform(0.05, 0.15)

    elif scenario == "COGNITIVE_LOAD":
        alpha_amplitude = 6.0
        beta_amplitude = 16.0
        theta_amplitude = 13.0

        alpha_power = random.uniform(0.20, 0.40)
        beta_power = random.uniform(0.75, 0.95)
        theta_power = random.uniform(0.70, 0.90)

        artifact_level = random.uniform(0.10, 0.22)

    elif scenario == "FATIGUED":
        alpha_amplitude = 5.0
        beta_amplitude = 5.0
        theta_amplitude = 17.0

        alpha_power = random.uniform(0.15, 0.35)
        beta_power = random.uniform(0.20, 0.40)
        theta_power = random.uniform(0.75, 0.95)

        artifact_level = random.uniform(0.15, 0.30)

    else:  # LOW_ENGAGEMENT
        alpha_amplitude = 10.0
        beta_amplitude = 2.5
        theta_amplitude = 3.0

        alpha_power = random.uniform(0.35, 0.50)
        beta_power = random.uniform(0.10, 0.25)
        theta_power = random.uniform(0.15, 0.30)

        artifact_level = random.uniform(0.05, 0.12)

    # ---------------------------------------------------------
    # Base EEG rhythms
    # ---------------------------------------------------------

    alpha = alpha_amplitude * np.sin(
        2 * np.pi * 10.0 * time_axis
    )

    beta = beta_amplitude * np.sin(
        2 * np.pi * 20.0 * time_axis + 0.7
    )

    theta = theta_amplitude * np.sin(
        2 * np.pi * 6.0 * time_axis + 1.2
    )

    # Slow baseline drift.
    drift = 2.0 * np.sin(
        2 * np.pi * 0.8 * time_axis
    )

    # Measurement noise.
    noise = np.random.normal(
        0.0,
        2.0,
        sample_count,
    )

    raw_waveform = (
        alpha
        + beta
        + theta
        + drift
        + noise
    )

    # ---------------------------------------------------------
    # Add transient artefact
    # ---------------------------------------------------------

    if random.random() < 0.35:
        start = random.randint(
            20,
            sample_count - 25,
        )

        width = random.randint(
            5,
            15,
        )

        artifact = np.linspace(
            0.0,
            random.uniform(25.0, 60.0),
            width,
        )

        raw_waveform[
            start:start + width
        ] += artifact

    # ---------------------------------------------------------
    # Filtering
    # ---------------------------------------------------------

    try:
        filtered_waveform = preprocess_eeg(
            raw_waveform,
            sampling_rate,
        )
    except ValueError:
        filtered_waveform = raw_waveform.copy()

    # ---------------------------------------------------------
    # Signal quality
    # ---------------------------------------------------------

    signal_quality = min(
        max(
            1.0 - artifact_level * 1.25,
            0.0,
        ),
        1.0,
    )

    # ---------------------------------------------------------
    # Return complete EEG snapshot
    # ---------------------------------------------------------

    return EEGSnapshot(
        sampling_rate_hz=sampling_rate,

        signal_quality=round(
            signal_quality,
            3,
        ),

        alpha_power=round(
            alpha_power,
            3,
        ),

        beta_power=round(
            beta_power,
            3,
        ),

        theta_power=round(
            theta_power,
            3,
        ),

        artifact_level=round(
            artifact_level,
            3,
        ),

        raw_waveform=[
            round(float(value), 4)
            for value in raw_waveform
        ],

        filtered_waveform=[
            round(float(value), 4)
            for value in filtered_waveform
        ],
    )