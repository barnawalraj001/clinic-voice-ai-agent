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