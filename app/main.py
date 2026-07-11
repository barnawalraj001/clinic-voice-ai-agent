import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.availability import router as availability_router
from app.routers.appointment import router as appointment_router
from app.routers.patients import router as patient_router
from app.routers.dashboard import router as dashboard_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(
    title="Clinic Voice AI Backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(availability_router)
app.include_router(appointment_router)
app.include_router(patient_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "message": "Clinic Voice AI Running"
    }