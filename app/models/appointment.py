from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patient_name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )

    doctor_id = Column(
        String,
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    availability_id = Column(
        Integer,
        ForeignKey("availability.id"),
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="BOOKED"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    doctor = relationship("Doctor")

    availability = relationship(
        "Availability",
        back_populates="appointment"
    )