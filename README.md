# Neuro-Adaptive Smart Activity

## Overview

**Neuro-Adaptive Smart Activity** is a research-oriented multimodal AI project that combines **physical activity recognition** with **brain-signal analysis** to estimate a user's overall state and provide adaptive, personalized responses.

The project explores how multiple human-signal modalities can be integrated into a single intelligent system rather than relying on physical activity or brain signals independently.

The current implementation provides a complete prototype pipeline with a Python backend, signal-processing components, state estimation, a monitoring dashboard, and a Unity-based interactive front end.

> **Research Prototype:** The current system includes synthetic/demo signal generation for development and demonstration. It should not be interpreted as a validated clinical or medical system.

---

## Research Concept

The core idea is to combine two complementary sources of information:

```text
        Physical Activity
               │
               ▼
      Activity Recognition
               │
               │
               ├──────────────┐
               │              │
               ▼              ▼
          Brain Signal    Physical State
               │              │
               ▼              │
        Signal Processing     │
               │              │
               ▼              │
         Brain Features       │
               │              │
               └──────┬───────┘
                      ▼
              Multimodal Fusion
                      │
                      ▼
              Human State Estimate
                      │
                      ▼
             Adaptive Response
````

The long-term research direction is to investigate whether multimodal information can provide a more informative representation of human state than any single modality alone.

---

## Key Features

### 🧠 Brain-Signal Analysis

The backend includes a signal-processing pipeline for brain-signal data, including:

* Signal generation
* Filtering
* Feature extraction
* Frequency-based analysis
* Brain-state estimation

The current prototype uses generated/demo signals so that the complete pipeline can be tested without requiring dedicated EEG hardware.

---

### 🏃 Physical Activity Recognition

The system models physical activity as a complementary modality to brain-signal information.

The architecture is designed to support activity classification and activity-state estimation before combining those signals with brain-state information.

---

### 🔬 Multimodal Fusion

The project combines information from multiple modalities to estimate an overall human state.

Conceptually:

```text
Brain State
     +
Activity State
     ↓
Multimodal Fusion
     ↓
Overall State
```

This architecture provides a foundation for comparing:

* Physical-only models
* Brain-only models
* Multimodal models

Such comparisons can be used to evaluate whether combining modalities provides useful additional information.

---

### 🤖 Adaptive Intelligence

The estimated human state can be used to drive an adaptive response.

For example:

```text
Sensor Signals
      ↓
Signal Processing
      ↓
State Estimation
      ↓
Adaptive Decision
      ↓
Personalized Response
```

The goal is to move beyond static activity recognition toward systems that can dynamically adapt to the user's estimated state.

---

### 📊 Monitoring Interface

The backend includes a browser-based monitoring interface for observing the system and its generated signals.

The interface is designed to make the prototype easier to demonstrate and debug while providing visibility into the underlying analysis pipeline.

---

### 🥽 Unity Interactive Front End

A Unity project is included as the interactive front-end component.

The Unity layer is intended to provide a more immersive visualization of the estimated human state and serves as the foundation for future smart-activity and adaptive-interaction scenarios.

---

## System Architecture

```text
┌───────────────────────────────┐
│        Signal Sources         │
│                               │
│  Physical Activity + Brain    │
│          Signals              │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Signal Processing       │
│                               │
│ Filtering / Feature Extraction│
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       State Estimation        │
│                               │
│ Brain State + Activity State  │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Multimodal Fusion       │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      Adaptive Intelligence    │
│                               │
│ Context-aware response logic  │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       User Interface          │
│                               │
│ Monitoring Dashboard / Unity  │
└───────────────────────────────┘
```

---

## Project Structure

```text
NeuroAdaptiveSmartActivity_Full/
│
├── Backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   ├── signal_processing/
│   │   │   ├── filters.py
│   │   │   ├── generator.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── static/
│   │   │   └── monitor.html
│   │   │
│   │   ├── main.py
│   │   └── __init__.py
│   │
│   ├── build/
│   ├── dist/
│   ├── requirements.txt
│   ├── run_backend.py
│   └── build_backend_exe.bat
│
├── Unity/
│   └── Unity project files
│
├── README.md
└── .gitignore
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* NumPy
* Signal-processing utilities

### Front End

* Unity
* C#

### Monitoring

* HTML
* JavaScript
* FastAPI-served interface

### Development

* Git
* GitHub
* PyInstaller

---

## Backend API

The backend runs locally using Uvicorn.

Default address:

```text
http://127.0.0.1:8000
```

The FastAPI application provides the backend services required by the monitoring and analysis pipeline.

The development API can be inspected through:

```text
http://127.0.0.1:8000/docs
```

Health/status endpoints and analysis functionality are implemented inside the backend application.

---

## Running the Backend

From the `Backend` directory:

### 1. Create a virtual environment

```powershell
python -m venv venv
```

### 2. Activate it

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start the backend

```powershell
python run_backend.py
```

The backend should become available at:

```text
http://127.0.0.1:8000
```

---

## Running the Monitoring Interface

Once the backend is running, open:

```text
http://127.0.0.1:8000/
```

The monitoring interface provides a browser-based view of the signal-analysis prototype.

---

## Unity Front End

The `Unity/` directory contains the interactive visualization layer.

The Unity application communicates with the backend to support the broader neuro-adaptive activity workflow.

The Unity project is intended to evolve into the primary visualization and interaction layer for:

* Activity visualization
* Brain-state visualization
* Multimodal state representation
* Adaptive feedback
* Future smart-device integration

---

## Research Motivation

Human activity and human cognitive state are closely related but cannot necessarily be represented using a single signal source.

A physical-activity-only system may capture what a person is doing, while brain-signal information can provide additional information about the internal state associated with that activity.

This project therefore investigates a multimodal approach:

```text
"What is the person doing?"
              +
"What is the person's estimated brain state?"
              ↓
     "What is the overall state?"
```

The resulting state can potentially support more context-aware and adaptive interaction systems.

---

## Research Questions

The project is designed around questions such as:

1. Can physical activity and brain-signal information be combined into a useful multimodal representation of human state?

2. Does multimodal fusion provide additional information compared with physical activity alone?

3. Does brain-signal information improve the interpretation of different physical activities?

4. Can estimated human state be used to dynamically adapt system behavior?

5. How can such systems be extended toward wearable devices and smart interfaces?

---

## Experimental Direction

A future experimental evaluation can compare three configurations:

```text
Model A → Physical Activity Only

Model B → Brain Signals Only

Model C → Physical Activity + Brain Signals
```

The three approaches can then be compared using appropriate classification and state-estimation metrics.

This provides a clearer research methodology than evaluating a multimodal system without single-modality baselines.

---

## Current Status

### Implemented

* Python backend
* FastAPI service
* Brain-signal generation pipeline
* Signal-processing components
* State-estimation components
* Browser monitoring interface
* Unity front end
* Backend executable build pipeline
* Structured project architecture

### Current Prototype Limitation

The present prototype uses **synthetic/demo signals** for development and system validation.

Therefore, the project does **not** claim experimental EEG findings or clinically validated brain-state measurements.

---

## Future Work

Potential extensions include:

* Integration with real EEG datasets
* Integration with wearable EEG hardware
* Real-world physical activity datasets
* More robust machine-learning models
* Temporal multimodal fusion
* Personalized state estimation
* Online/adaptive learning
* Validation with human participants
* Smart-glasses or wearable HUD integration
* Real-time adaptive coaching
* More advanced Unity visualization
* Experimental comparison of unimodal and multimodal models

---

## Research Pipeline

The intended long-term pipeline is:

```text
Real-World Sensor Data
        ↓
Data Preprocessing
        ↓
Feature Extraction
        ↓
Activity Recognition
        +
Brain-Signal Analysis
        ↓
Multimodal Fusion
        ↓
Human-State Estimation
        ↓
Adaptive Decision Making
        ↓
Personalized Interaction
```

---

## Why This Project Matters

The broader objective is to explore how AI systems can become more **context-aware, multimodal, and adaptive** by combining different types of human data.

Instead of treating activity recognition and brain-signal analysis as separate problems, the project investigates a unified architecture where both contribute to a shared estimate of human state.

This direction is relevant to research in:

* Multimodal AI
* Human-centered AI
* Brain-computer interfaces
* Wearable computing
* Adaptive interfaces
* Intelligent physical-activity systems
* Human-AI interaction

---

## Disclaimer

This project is a research and software-development prototype.

The current implementation is intended for experimentation, demonstration, and system development. It is **not a medical device**, diagnostic system, or clinically validated brain-state measurement platform.

---

## Author

**Aditya Pawar**

