from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.appointment import (
    BookAppointmentRequest,
    BookAppointmentResponse,
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    RescheduleAppointmentRequest,
    RescheduleAppointmentResponse,
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


@router.post(
    "/cancel",
    response_model=CancelAppointmentResponse,
)
def cancel_appointment(
    request: CancelAppointmentRequest,
    db: Session = Depends(get_db),
):

    return BookingService.cancel_appointment(
        db=db,
        appointment_id=request.appointment_id,
    )

@router.post(
    "/reschedule",
    response_model=RescheduleAppointmentResponse,
)
def reschedule_appointment(
    request: RescheduleAppointmentRequest,
    db: Session = Depends(get_db),
):
    return BookingService.reschedule_appointment(
        db=db,
        appointment_id=request.appointment_id,
        new_availability_id=request.new_availability_id,
    )