from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="Neuro-Adaptive Backend",
    version="0.1.0",
    description="Multimodal physical activity and brain signal research prototype backend.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health():
    return {
        "status": "online",
        "service": "neuro-adaptive-backend",
        "version": "0.1.0",
    }
