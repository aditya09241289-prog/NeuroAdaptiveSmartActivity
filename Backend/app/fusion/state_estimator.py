from dataclasses import dataclass
from typing import Dict, List, Tuple

from app.models.schemas import (
    ActivitySnapshot,
    EEGSnapshot,
    ExperimentalState,
)


@dataclass
class FusionFeatures:
    alpha: float
    beta: float
    theta: float
    signal_quality: float
    artifact_level: float

    heart_rate: float
    speed: float
    effort: float
    fatigue: float


def clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 1.0,
) -> float:
    return max(
        minimum,
        min(value, maximum),
    )


def normalize_range(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    if maximum <= minimum:
        return 0.0

    return clamp(
        (value - minimum) / (maximum - minimum)
    )


def build_fusion_features(
    eeg: EEGSnapshot,
    activity: ActivitySnapshot,
) -> FusionFeatures:

    return FusionFeatures(
        alpha=clamp(eeg.alpha_power),
        beta=clamp(eeg.beta_power),
        theta=clamp(eeg.theta_power),

        signal_quality=clamp(
            eeg.signal_quality
        ),

        artifact_level=clamp(
            eeg.artifact_level
        ),

        heart_rate=normalize_range(
            activity.heart_rate_bpm,
            50.0,
            190.0,
        ),

        speed=normalize_range(
            activity.speed_kmh,
            0.0,
            20.0,
        ),

        effort=clamp(
            activity.effort
        ),

        fatigue=clamp(
            activity.fatigue
        ),
    )


def compute_state_scores(
    features: FusionFeatures,
) -> Dict[str, float]:

    # ---------------------------------------------------------
    # FOCUSED
    # ---------------------------------------------------------

    focused_score = (
        0.40 * features.alpha
        + 0.25 * features.signal_quality
        + 0.15 * (1.0 - features.artifact_level)
        + 0.20 * (1.0 - features.fatigue)
    )

    # ---------------------------------------------------------
    # COGNITIVE LOAD
    # ---------------------------------------------------------

    cognitive_load_score = (
        0.30 * features.beta
        + 0.25 * features.theta
        + 0.20 * features.effort
        + 0.15 * features.heart_rate
        + 0.10 * features.artifact_level
    )

    # ---------------------------------------------------------
    # FATIGUED
    # ---------------------------------------------------------

    fatigue_score = (
        0.45 * features.fatigue
        + 0.20 * features.effort
        + 0.15 * features.heart_rate
        + 0.10 * features.speed
        + 0.10 * (1.0 - features.signal_quality)
    )

    # ---------------------------------------------------------
    # LOW ENGAGEMENT
    #
    # Stronger separation from NORMAL:
    #   - low effort
    #   - low speed
    #   - low relative HR
    #   - low beta
    # ---------------------------------------------------------

    low_engagement_score = (
        0.40 * (1.0 - features.effort)
        + 0.25 * (1.0 - features.speed)
        + 0.20 * (1.0 - features.heart_rate)
        + 0.15 * (1.0 - features.beta)
    )

    # Extra low-engagement boost when several
    # low-activity indicators agree.
    low_activity_signal = (
        (1.0 - features.effort)
        * (1.0 - features.speed)
        * (1.0 - features.heart_rate)
    )

    low_engagement_score += (
        0.15 * low_activity_signal
    )

    low_engagement_score = clamp(
        low_engagement_score
    )

    # ---------------------------------------------------------
    # NORMAL
    #
    # Keep NORMAL strongest around intermediate effort,
    # intermediate fatigue, and balanced EEG.
    # ---------------------------------------------------------

    effort_balance = clamp(
        1.0 - abs(
            features.effort - 0.52
        ) / 0.52
    )

    fatigue_balance = clamp(
        1.0 - abs(
            features.fatigue - 0.35
        ) / 0.65
    )

    eeg_balance = clamp(
        1.0 - abs(
            features.alpha - features.beta
        )
    )

    normal_score = (
        0.30 * effort_balance
        + 0.25 * fatigue_balance
        + 0.20 * features.signal_quality
        + 0.15 * (1.0 - features.artifact_level)
        + 0.10 * eeg_balance
    )

    # Penalize NORMAL when activity is clearly very low.
    very_low_activity = (
        (features.effort < 0.35)
        and (features.speed < 0.40)
    )

    if very_low_activity:
        normal_score *= 0.75

    normal_score = clamp(
        normal_score
    )

    return {
        "FOCUSED": focused_score,
        "COGNITIVE_LOAD": cognitive_load_score,
        "FATIGUED": fatigue_score,
        "LOW_ENGAGEMENT": low_engagement_score,
        "NORMAL": normal_score,
    }


def choose_state(
    scores: Dict[str, float],
) -> Tuple[str, float]:

    ordered = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    best_state, best_score = ordered[0]

    second_score = (
        ordered[1][1]
        if len(ordered) > 1
        else 0.0
    )

    margin = max(
        best_score - second_score,
        0.0,
    )

    confidence = clamp(
        0.55 + 0.45 * margin
    )

    return (
        best_state,
        confidence,
    )


def build_rationale(
    state: str,
    features: FusionFeatures,
) -> List[str]:

    rationale: List[str] = []

    if state == "FOCUSED":

        if features.alpha >= 0.65:
            rationale.append(
                "Strong alpha activity."
            )

        if features.signal_quality >= 0.70:
            rationale.append(
                "Good EEG signal quality."
            )

        if features.artifact_level <= 0.15:
            rationale.append(
                "Low signal artifact level."
            )

        if features.fatigue <= 0.35:
            rationale.append(
                "Low physical fatigue."
            )

        if features.effort >= 0.45:
            rationale.append(
                "Moderate physical engagement."
            )

    elif state == "COGNITIVE_LOAD":

        if features.beta >= 0.65:
            rationale.append(
                "Elevated beta activity."
            )

        if features.theta >= 0.60:
            rationale.append(
                "Elevated theta activity."
            )

        if features.effort >= 0.65:
            rationale.append(
                "High physical effort."
            )

        if features.heart_rate >= 0.60:
            rationale.append(
                "Elevated relative heart rate."
            )

    elif state == "FATIGUED":

        if features.fatigue >= 0.70:
            rationale.append(
                "High estimated fatigue."
            )

        if features.effort >= 0.65:
            rationale.append(
                "Sustained high physical effort."
            )

        if features.heart_rate >= 0.65:
            rationale.append(
                "Elevated relative heart rate."
            )

        if features.signal_quality < 0.70:
            rationale.append(
                "Reduced EEG signal quality."
            )

    elif state == "LOW_ENGAGEMENT":

        if features.effort <= 0.35:
            rationale.append(
                "Low physical effort."
            )

        if features.speed <= 0.40:
            rationale.append(
                "Low movement intensity."
            )

        if features.heart_rate <= 0.40:
            rationale.append(
                "Low relative heart rate."
            )

        if features.beta <= 0.30:
            rationale.append(
                "Low beta activity."
            )

    elif state == "NORMAL":

        if 0.30 <= features.fatigue <= 0.65:
            rationale.append(
                "Moderate fatigue level."
            )

        if 0.35 <= features.effort <= 0.70:
            rationale.append(
                "Moderate activity effort."
            )

        if features.signal_quality >= 0.65:
            rationale.append(
                "Acceptable EEG signal quality."
            )

    if not rationale:
        rationale.append(
            "State selected from combined EEG and "
            "physical-activity features."
        )

    return rationale


def get_coaching_message(
    state: str,
) -> str:

    messages = {
        "FOCUSED":
            "Stay focused and maintain your current pace.",

        "COGNITIVE_LOAD":
            "Simplify guidance and focus on one task at a time.",

        "FATIGUED":
            "Reduce intensity and maintain a steady rhythm.",

        "LOW_ENGAGEMENT":
            "Increase activity gradually if appropriate.",

        "NORMAL":
            "Maintain a comfortable and sustainable pace.",
    }

    return messages.get(
        state,
        "Continue at a comfortable pace.",
    )


def estimate_experimental_state(
    eeg: EEGSnapshot,
    activity: ActivitySnapshot,
) -> ExperimentalState:

    features = build_fusion_features(
        eeg,
        activity,
    )

    scores = compute_state_scores(
        features
    )

    state, confidence = choose_state(
        scores
    )

    rationale = build_rationale(
        state,
        features
    )

    return ExperimentalState(
        label=state,
        confidence=round(
            confidence,
            3,
        ),
        coaching_message=
            get_coaching_message(state),
        rationale=rationale,
    )