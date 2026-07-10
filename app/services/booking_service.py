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