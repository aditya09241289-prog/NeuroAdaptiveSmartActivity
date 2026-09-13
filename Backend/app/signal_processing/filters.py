import numpy as np
from scipy.signal import butter, filtfilt, iirnotch


def bandpass_filter(
    signal: np.ndarray,
    sampling_rate: float,
    low_cutoff: float = 0.5,
    high_cutoff: float = 45.0,
    order: int = 4,
) -> np.ndarray:
    nyquist = sampling_rate * 0.5

    low = low_cutoff / nyquist
    high = high_cutoff / nyquist

    if not 0.0 < low < high < 1.0:
        raise ValueError("Invalid band-pass cutoff frequencies.")

    b, a = butter(
        order,
        [low, high],
        btype="band",
    )

    return filtfilt(b, a, signal)


def notch_filter(
    signal: np.ndarray,
    sampling_rate: float,
    notch_frequency: float = 50.0,
    quality_factor: float = 30.0,
) -> np.ndarray:
    nyquist = sampling_rate * 0.5
    normalized_frequency = notch_frequency / nyquist

    if not 0.0 < normalized_frequency < 1.0:
        raise ValueError("Invalid notch frequency.")

    b, a = iirnotch(
        normalized_frequency,
        quality_factor,
    )

    return filtfilt(b, a, signal)


def preprocess_eeg(
    signal: np.ndarray,
    sampling_rate: float,
) -> np.ndarray:
    filtered = bandpass_filter(
        signal,
        sampling_rate,
        low_cutoff=0.5,
        high_cutoff=45.0,
    )

    filtered = notch_filter(
        filtered,
        sampling_rate,
        notch_frequency=50.0,
    )

    return filtered