from sqlalchemy.orm import Session

from app.models.appointment import Appointment


class PatientService:

    @staticmethod
    def search_patient(
        db: Session,
        phone: str,
    ):

        appointments = (
            db.query(Appointment)
            .filter(Appointment.phone == phone)
            .order_by(Appointment.created_at.desc())
            .all()
        )

        if not appointments:
            return {
                "found": False,
                "message": "No previous appointments found."
            }

        latest = appointments[0]

        slot = latest.availability
        doctor = slot.doctor
        branch = doctor.branch

        return {
            "found": True,
            "patient_name": latest.patient_name,
            "appointment_count": len(appointments),
            "last_appointment": {
                "appointment_id": latest.appointment_id,
                "doctor": doctor.name,
                "specialty": doctor.specialty,
                "branch": branch.name,
                "date": slot.date.isoformat(),
                "time": slot.start_time.strftime("%H:%M"),
            }
        }