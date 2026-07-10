from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.appointment import (
    BookAppointmentRequest,
    BookAppointmentResponse,
)
from app.services.booking_service import BookingService

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.post(
    "/book",
    response_model=BookAppointmentResponse,
)
def book_appointment(
    request: BookAppointmentRequest,
    db: Session = Depends(get_db),
):

    return BookingService.book_appointment(
        db=db,
        availability_id=request.availability_id,
        patient_name=request.patient_name,
        phone=request.phone,
    )