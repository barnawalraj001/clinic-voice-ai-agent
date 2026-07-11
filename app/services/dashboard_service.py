from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import (
    Doctor,
    Branch,
    Appointment,
    Availability,
)


class DashboardService:

    @staticmethod
    def get_stats(db: Session):

        total_doctors = db.query(Doctor).count()

        total_branches = db.query(Branch).count()

        total_patients = (
            db.query(Appointment.phone)
            .distinct()
            .count()
        )

        total_appointments = (
            db.query(Appointment)
            .count()
        )

        booked_appointments = (
            db.query(Appointment)
            .filter(Appointment.status == "BOOKED")
            .count()
        )

        cancelled_appointments = (
            db.query(Appointment)
            .filter(Appointment.status == "CANCELLED")
            .count()
        )

        available_slots = (
            db.query(Availability)
            .filter(Availability.is_booked == False)
            .count()
        )

        booked_slots = (
            db.query(Availability)
            .filter(Availability.is_booked == True)
            .count()
        )

        return {
            "total_doctors": total_doctors,
            "total_branches": total_branches,
            "total_patients": total_patients,
            "total_appointments": total_appointments,
            "booked_appointments": booked_appointments,
            "cancelled_appointments": cancelled_appointments,
            "available_slots": available_slots,
            "booked_slots": booked_slots,
        }

    @staticmethod
    def get_appointments(db: Session):

        appointments = (
            db.query(
                Appointment,
                Availability,
                Doctor,
                Branch,
            )
            .join(
                Availability,
                Appointment.availability_id == Availability.id,
            )
            .join(
                Doctor,
                Appointment.doctor_id == Doctor.doctor_id,
            )
            .join(
                Branch,
                Doctor.branch_id == Branch.branch_id,
            )
            .order_by(
                Appointment.created_at.desc()
            )
            .all()
        )

        result = []

        for appointment, availability, doctor, branch in appointments:

            result.append(
                {
                    "appointment_id": appointment.appointment_id,
                    "patient_name": appointment.patient_name,
                    "phone": appointment.phone,
                    "doctor": doctor.name,
                    "specialty": doctor.specialty,
                    "branch": branch.name,
                    "date": availability.date,
                    "time": availability.start_time,
                    "status": appointment.status,
                    "created_at": appointment.created_at,
                }
            )

        return {
            "appointments": result
        }

    @staticmethod
    def get_availability(db: Session):

        slots = (
            db.query(
                Availability,
                Doctor,
                Branch,
            )
            .join(
                Doctor,
                Availability.doctor_id == Doctor.doctor_id,
            )
            .join(
                Branch,
                Doctor.branch_id == Branch.branch_id,
            )
            .order_by(
                Availability.date,
                Availability.start_time,
            )
            .all()
        )

        result = []

        for availability, doctor, branch in slots:

            result.append(
                {
                    "availability_id": availability.id,
                    "doctor": doctor.name,
                    "specialty": doctor.specialty,
                    "branch": branch.name,
                    "date": availability.date,
                    "start_time": availability.start_time,
                    "end_time": availability.end_time,
                    "is_booked": availability.is_booked,
                }
            )

        return {
            "availability": result
        }


    @staticmethod
    def get_doctors(db: Session):

        doctors = (
            db.query(
                Doctor,
                Branch,
            )
            .join(
                Branch,
                Doctor.branch_id == Branch.branch_id,
            )
            .all()
        )

        result = []

        for doctor, branch in doctors:

            total_slots = (
                db.query(Availability)
                .filter(
                    Availability.doctor_id == doctor.doctor_id
                )
                .count()
            )

            booked_slots = (
                db.query(Availability)
                .filter(
                    Availability.doctor_id == doctor.doctor_id,
                    Availability.is_booked == True,
                )
                .count()
            )

            result.append(
                {
                    "doctor_id": doctor.doctor_id,
                    "name": doctor.name,
                    "specialty": doctor.specialty,
                    "experience_years": doctor.experience_years,
                    "branch": branch.name,
                    "total_slots": total_slots,
                    "booked_slots": booked_slots,
                }
            )

        return {
            "doctors": result
        }



    @staticmethod
    def get_patients(db: Session):

        phones = (
            db.query(Appointment.phone)
            .distinct()
            .all()
        )

        result = []

        for (phone,) in phones:

            appointments = (
                db.query(Appointment)
                .filter(
                    Appointment.phone == phone
                )
                .order_by(
                    Appointment.created_at.desc()
                )
                .all()
            )

            latest = appointments[0]

            availability = (
                db.query(Availability)
                .filter(
                    Availability.id == latest.availability_id
                )
                .first()
            )

            doctor = (
                db.query(Doctor)
                .filter(
                    Doctor.doctor_id == latest.doctor_id
                )
                .first()
            )
            branch = (
                db.query(Branch)
                .filter(
                    Branch.branch_id == doctor.branch_id
                )
                .first()
            )
            result.append(
                {
                    "patient_name": latest.patient_name,
                    "phone": phone,
                    "appointment_count": len(appointments),
                    "latest_appointment": availability.date,
                    "latest_doctor": doctor.name,
                    "latest_specialty": doctor.specialty,
                    "latest_branch": branch.name,
                    "latest_time": availability.start_time,
                }
            )

        return {
            "patients": result
        }