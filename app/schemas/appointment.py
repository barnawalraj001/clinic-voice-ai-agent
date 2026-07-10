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


class CancelAppointmentRequest(BaseModel):
    appointment_id: int


class CancelAppointmentResponse(BaseModel):
    success: bool
    message: str


class RescheduleAppointmentRequest(BaseModel):
    appointment_id: int
    new_availability_id: int


class RescheduleAppointmentResponse(BaseModel):
    success: bool
    appointment_id: int
    doctor: str
    branch: str
    date: str
    time: str
    message: str