from fastapi import HTTPException
from sqlalchemy.orm import Session

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
                detail="Availability slot not found."
            )

        if slot.is_booked:
            raise HTTPException(
                status_code=409,
                detail="This slot is already booked."
            )

        appointment = Appointment(
            patient_name=patient_name,
            phone=phone,
            doctor_id=slot.doctor_id,
            availability_id=slot.id,
            status="BOOKED",
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
                detail="Appointment not found."
            )

        if appointment.status == "CANCELLED":
            raise HTTPException(
                status_code=409,
                detail="Appointment is already cancelled."
            )

        slot = appointment.availability

        appointment.status = "CANCELLED"

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
        # Find appointment
        appointment = (
            db.query(Appointment)
            .filter(Appointment.appointment_id == appointment_id)
            .first()
        )

        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found."
            )

        if appointment.status == "CANCELLED":
            raise HTTPException(
                status_code=409,
                detail="Cancelled appointments cannot be rescheduled."
            )

        # Current slot
        old_slot = appointment.availability

        # New slot
        new_slot = (
            db.query(Availability)
            .filter(Availability.id == new_availability_id)
            .first()
        )

        if new_slot is None:
            raise HTTPException(
                status_code=404,
                detail="Requested availability slot not found."
            )

        if new_slot.is_booked:
            raise HTTPException(
                status_code=409,
                detail="Requested slot is already booked."
            )

        # Release old slot
        old_slot.is_booked = False

        # Reserve new slot
        new_slot.is_booked = True

        # Update appointment
        appointment.availability_id = new_slot.id
        appointment.doctor_id = new_slot.doctor_id
        appointment.status = "BOOKED"

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