from fastapi import FastAPI

from app.routers.availability import router as availability_router

app = FastAPI(
    title="Clinic Voice AI Backend"
)

app.include_router(availability_router)


@app.get("/")
def root():
    return {
        "message": "Clinic Voice AI Running"
    }