from pydantic import BaseModel
from datetime import datetime, date, time
from typing import List


class AvailabilityRow(BaseModel):
    availability_id: int
    doctor: str
    specialty: str
    branch: str
    date: date
    start_time: time
    end_time: time
    is_booked: bool


class AvailabilityListResponse(BaseModel):
    availability: List[AvailabilityRow]


class AppointmentRow(BaseModel):
    appointment_id: int
    patient_name: str
    phone: str
    doctor: str
    specialty: str
    branch: str
    date: date
    time: time
    status: str
    created_at: datetime


class AppointmentListResponse(BaseModel):
    appointments: List[AppointmentRow]

class DashboardStatsResponse(BaseModel):
    total_doctors: int
    total_branches: int
    total_patients: int
    total_appointments: int
    booked_appointments: int
    cancelled_appointments: int
    available_slots: int
    booked_slots: int


class DoctorRow(BaseModel):
    doctor_id: str
    name: str
    specialty: str
    experience_years: int | None
    branch: str
    total_slots: int
    booked_slots: int


class DoctorListResponse(BaseModel):
    doctors: list[DoctorRow]

class PatientRow(BaseModel):
    patient_name: str
    phone: str
    appointment_count: int
    latest_appointment: date
    latest_doctor: str
    latest_specialty: str
    latest_branch: str
    latest_time: time


class PatientListResponse(BaseModel):
    patients: list[PatientRow]