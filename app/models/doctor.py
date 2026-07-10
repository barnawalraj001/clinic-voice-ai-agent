from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)

    branch_id = Column(
        String,
        ForeignKey("branches.branch_id")
    )

    experience_years = Column(Integer)

    branch = relationship(
        "Branch",
        back_populates="doctors"
    )

    availability = relationship(
        "Availability",
        back_populates="doctor"
    )