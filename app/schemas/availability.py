from datetime import date as DateType
from datetime import time as TimeType
from typing import Optional

from pydantic import BaseModel


class AvailabilitySearchRequest(BaseModel):
    specialty: Optional[str] = None
    branch: Optional[str] = None
    date: Optional[DateType] = None
    preferred_time: Optional[TimeType] = None


class SlotResponse(BaseModel):
    doctor_name: str
    specialty: str
    branch: str
    date: DateType
    start_time: TimeType
    end_time: TimeType


class AvailabilitySearchResponse(BaseModel):
    count: int
    available_slots: list[SlotResponse]