from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.availability import (
    AvailabilitySearchRequest,
    AvailabilitySearchResponse,
    SlotResponse,
)
from app.services.availability_service import search_availability

router = APIRouter(
    prefix="/availability",
    tags=["Availability"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/search", response_model=AvailabilitySearchResponse)
def search_slots(
    request: AvailabilitySearchRequest,
    db: Session = Depends(get_db),
):

    results = search_availability(
        db=db,
        specialty=request.specialty,
        branch=request.branch,
        date=request.date,
        preferred_time=request.preferred_time,
    )

    slots = []

    for availability, doctor, branch in results:

        slots.append(
            SlotResponse(
                doctor_name=doctor.name,
                specialty=doctor.specialty,
                branch=branch.name,
                date=availability.date,
                start_time=availability.start_time,
                end_time=availability.end_time,
            )
        )

    return AvailabilitySearchResponse(
        count=len(slots),
        available_slots=slots
    )