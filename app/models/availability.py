from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, autoincrement=True)

    doctor_id = Column(
        String,
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    date = Column(Date, nullable=False)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)

    is_booked = Column(Boolean, default=False)
    
    doctor = relationship("Doctor", back_populates="availability")