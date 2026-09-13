from fastapi import APIRouter

from app.models.schemas import HealthSampleResponse
from app.signal_processing.generator import generate_synthetic_eeg_snapshot
from app.activity.simulator import generate_activity_snapshot
from app.fusion.state_estimator import estimate_experimental_state

router = APIRouter()


@router.get("/session/sample", response_model=HealthSampleResponse)
def get_session_sample():
    eeg = generate_synthetic_eeg_snapshot()
    activity = generate_activity_snapshot()
    state = estimate_experimental_state(eeg, activity)

    return HealthSampleResponse(
        eeg=eeg,
        activity=activity,
        estimated_state=state,
    )
