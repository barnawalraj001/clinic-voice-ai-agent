from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.constants.appointment_errors import (
    APPOINTMENT_ALREADY_CANCELLED,
    APPOINTMENT_NOT_FOUND,
    AVAILABILITY_SLOT_NOT_FOUND,
    CANCELLED_APPOINTMENT_CANNOT_RESCHEDULE,
    REQUESTED_AVAILABILITY_SLOT_NOT_FOUND,
    REQUESTED_SLOT_ALREADY_BOOKED,
    SLOT_ALREADY_BOOKED,
)
from app.enums.appointment_status import AppointmentStatus
from app.models.availability import Availability
from app.models.appointment import Appointment


class BookingService:

    @staticmethod
    def book_appointment(
        db: Session,
        availability_id: int,
        patient_name: str,
        phone: str,
    ):

        slot = (
            db.query(Availability)
            .filter(Availability.id == availability_id)
            .first()
        )

        if slot is None:
            raise HTTPException(
                status_code=404,
                detail=AVAILABILITY_SLOT_NOT_FOUND,
            )

        if slot.is_booked:
            raise HTTPException(
                status_code=409,
                detail=SLOT_ALREADY_BOOKED,
            )

        appointment = Appointment(
            patient_name=patient_name,
            phone=phone,
            doctor_id=slot.doctor_id,
            availability_id=slot.id,
            status=AppointmentStatus.BOOKED.value,
        )

        db.add(appointment)

        slot.is_booked = True

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(appointment)

        return {
            "success": True,
            "appointment_id": appointment.appointment_id,
            "doctor": slot.doctor.name,
            "branch": slot.doctor.branch.name,
            "date": slot.date.isoformat(),
            "time": slot.start_time.strftime("%H:%M"),
            "message": "Appointment booked successfully."
        }

    @staticmethod
    def cancel_appointment(
        db: Session,
        appointment_id: int,
    ):

        appointment = (
            db.query(Appointment)
            .filter(
                Appointment.appointment_id == appointment_id
            )
            .first()
        )

        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail=APPOINTMENT_NOT_FOUND,
            )

        if appointment.status == AppointmentStatus.CANCELLED.value:
            raise HTTPException(
                status_code=409,
                detail=APPOINTMENT_ALREADY_CANCELLED,
            )

        slot = appointment.availability

        appointment.status = AppointmentStatus.CANCELLED.value

        slot.is_booked = False

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return {
            "success": True,
            "message": "Appointment cancelled successfully."
        }

    @staticmethod
    def reschedule_appointment(
        db: Session,
        appointment_id: int,
        new_availability_id: int,
    ):
        appointment = (
            db.query(Appointment)
            .filter(Appointment.appointment_id == appointment_id)
            .first()
        )

        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail=APPOINTMENT_NOT_FOUND,
            )

        if appointment.status == AppointmentStatus.CANCELLED.value:
            raise HTTPException(
                status_code=409,
                detail=CANCELLED_APPOINTMENT_CANNOT_RESCHEDULE,
            )

        old_slot = appointment.availability

        new_slot = (
            db.query(Availability)
            .filter(Availability.id == new_availability_id)
            .first()
        )

        if new_slot is None:
            raise HTTPException(
                status_code=404,
                detail=REQUESTED_AVAILABILITY_SLOT_NOT_FOUND,
            )

        if new_slot.is_booked:
            raise HTTPException(
                status_code=409,
                detail=REQUESTED_SLOT_ALREADY_BOOKED,
            )

        old_slot.is_booked = False

        new_slot.is_booked = True

        appointment.availability_id = new_slot.id
        appointment.doctor_id = new_slot.doctor_id
        appointment.status = AppointmentStatus.BOOKED.value

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(appointment)

        return {
            "success": True,
            "appointment_id": appointment.appointment_id,
            "doctor": new_slot.doctor.name,
            "branch": new_slot.doctor.branch.name,
            "date": new_slot.date.isoformat(),
            "time": new_slot.start_time.strftime("%H:%M"),
            "message": "Appointment rescheduled successfully."
        }
