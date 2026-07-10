from pydantic import BaseModel


class SearchPatientRequest(BaseModel):
    phone: str


class LastAppointment(BaseModel):
    appointment_id: int
    doctor: str
    specialty: str
    branch: str
    date: str
    time: str


class SearchPatientResponse(BaseModel):
    found: bool
    patient_name: str | None = None
    appointment_count: int | None = None
    last_appointment: LastAppointment | None = None
    message: str | None = None