from typing import List, Literal

from pydantic import BaseModel, Field


class EEGSnapshot(BaseModel):
    sampling_rate_hz: int = Field(..., ge=1)

    signal_quality: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    alpha_power: float
    beta_power: float
    theta_power: float

    artifact_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    raw_waveform: List[float]
    filtered_waveform: List[float]


class ActivitySnapshot(BaseModel):
    activity: Literal[
        "running",
        "cycling",
        "gym",
    ]

    # Development ground-truth scenario.
    scenario: str = ""

    heart_rate_bpm: float = Field(
        ...,
        ge=0.0,
    )

    speed_kmh: float = Field(
        ...,
        ge=0.0,
    )

    effort: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    fatigue: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )


class ExperimentalState(BaseModel):
    label: Literal[
        "FOCUSED",
        "NORMAL",
        "COGNITIVE_LOAD",
        "FATIGUED",
        "LOW_ENGAGEMENT",
    ]

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    coaching_message: str

    rationale: List[str] = Field(
        default_factory=list
    )


class HealthSampleResponse(BaseModel):
    eeg: EEGSnapshot
    activity: ActivitySnapshot
    estimated_state: ExperimentalState