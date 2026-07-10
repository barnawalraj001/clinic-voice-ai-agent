from fastapi import FastAPI

from app.routers.availability import router as availability_router
from app.routers.appointment import router as appointment_router
from app.routers.patients import router as patient_router

app = FastAPI(
    title="Clinic Voice AI Backend"
)

app.include_router(availability_router)
app.include_router(appointment_router)
app.include_router(patient_router)


@app.get("/")
def root():
    return {
        "message": "Clinic Voice AI Running"
    }