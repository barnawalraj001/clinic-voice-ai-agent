from pydantic import BaseModel


class BookAppointmentRequest(BaseModel):
    availability_id: int
    patient_name: str
    phone: str


class BookAppointmentResponse(BaseModel):
    success: bool
    appointment_id: int
    doctor: str
    branch: str
    date: str
    time: str
    message: str