# Neuro-Adaptive Smart Physical Activity + Brain Signal Analysis

## Overview

This project is a research-oriented prototype that combines simulated brain-signal data and physical activity data to estimate a person's current neuro-adaptive state.

The system consists of a Unity-based interactive frontend and a FastAPI backend. The backend generates synthetic EEG and activity data, processes the information, and performs multimodal fusion to estimate an experimental state.

The Unity application visualizes the estimated state, displays EEG and physical activity metrics, provides adaptive coaching feedback, and records session data for evaluation.

> This is a controlled synthetic research prototype. It is not a clinical or medical diagnostic system.

---

## Architecture

```text
Unity Frontend
      │
      │ HTTP / JSON
      ▼
FastAPI Backend
      │
      ├── Synthetic EEG Generation
      ├── Activity Simulation
      ├── Signal Processing
      └── Multimodal State Estimation
      │
      ▼
Neuro-Adaptive State
      │
      ▼
Unity Visualization + Session Logging
      │
      ├── CSV Session Log
      ├── Session Summary
      └── Session Evaluation
```

---

## Experimental States

The multimodal fusion system estimates one of five experimental states:

- **FOCUSED**
- **NORMAL**
- **COGNITIVE_LOAD**
- **FATIGUED**
- **LOW_ENGAGEMENT**

Each prediction includes:

- Estimated state
- Confidence score
- Adaptive coaching message
- Fusion rationale

---

## Technology Stack

### Frontend
- Unity 6
- C#
- Universal 3D / URP

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### Processing
- Synthetic EEG signal generation
- EEG feature representation
- Signal quality estimation
- Artifact estimation
- Physical activity simulation
- Multimodal state fusion

---

## Backend API

### Health Check

```text
GET /health
```

### Session Sample

```text
GET /api/v1/session/sample
```

The session endpoint returns:

- Synthetic EEG snapshot
- Physical activity snapshot
- Synthetic experimental scenario
- Estimated neuro-adaptive state

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Running the Backend

Open a terminal inside:

```text
Backend/
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend:

```bash
python run_backend.py
```

The backend will run at:

```text
http://127.0.0.1:8000
```

---

## Running the Unity Application

Open the Unity project and press **Play**.

The Unity application connects to the FastAPI backend and continuously requests neuro-adaptive samples.

Expected console messages:

```text
[NeuroAdaptive] Application manager initialized.
[NeuroAdaptive] BACKEND ONLINE ...
[NeuroAdaptive] SAMPLE RECEIVED
State: FOCUSED
```

---

## Session Recording

During execution, the application records neuro-adaptive session samples.

The recorded information includes:

- Timestamp
- Expected synthetic scenario
- Predicted state
- Prediction confidence
- EEG features
- Activity type
- Heart rate
- Speed
- Effort
- Fatigue

The system generates:

```text
neuro_adaptive_session.csv
neuro_adaptive_session_summary.txt
neuro_adaptive_session_evaluation.txt
```

---

## Session Evaluation

The evaluation compares the synthetic scenario used to generate a sample with the state predicted by the multimodal fusion system.

The generated evaluation includes:

- Number of valid samples
- Correct predictions
- Overall accuracy
- Mean confidence
- Per-state accuracy
- Confusion matrix

Example development result:

```text
Overall accuracy: 96.3%
Mean confidence: 60.7%
```

---

## Important Limitation

The current evaluation uses controlled synthetic development scenarios.

Therefore:

```text
Expected state = synthetic scenario
Predicted state = multimodal fusion result
```

The reported accuracy represents performance within the controlled synthetic environment.

It does **not** represent clinical EEG classification accuracy, medical diagnostic performance, or validated real-world performance.

Further validation would require real EEG recordings, labeled experimental data, multiple participants, and independent testing.

---

## Project Structure

```text
NeuroAdaptiveSmartActivity_Full/
│
├── Backend/
│   ├── app/
│   ├── requirements.txt
│   └── run_backend.py
│
├── Brain Analysis/
│   ├── neuro_adaptive_session.csv
│   ├── neuro_adaptive_session_summary.txt
│   └── neuro_adaptive_session_evaluation.txt
│
├── Unity/
│
└── README.md
```

---

## Current Status

- [x] Unity frontend
- [x] FastAPI backend
- [x] Synthetic EEG generation
- [x] Physical activity simulation
- [x] Multimodal state estimation
- [x] Adaptive coaching
- [x] Backend-to-Unity communication
- [x] Session logging
- [x] Session summary generation
- [x] Automated evaluation
- [x] Per-state accuracy analysis
- [x] Confusion matrix generation