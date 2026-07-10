from sqlalchemy import Column, String, Integer, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    branch_id = Column(String, ForeignKey("branches.branch_id"))
    experience_years = Column(Integer)
    availability = relationship("Availability", back_populates="doctor")