from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.schemas.dashboard import DashboardStatsResponse
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import (
    DashboardStatsResponse,
    AppointmentListResponse,
    AvailabilityListResponse,
    DoctorListResponse,
    PatientListResponse,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
)
def dashboard_stats(
    db: Session = Depends(get_db),
):

    return DashboardService.get_stats(db)

@router.get(
    "/appointments",
    response_model=AppointmentListResponse,
)
def dashboard_appointments(
    db: Session = Depends(get_db),
):

    return DashboardService.get_appointments(db)

@router.get(
    "/availability",
    response_model=AvailabilityListResponse,
)
def dashboard_availability(
    db: Session = Depends(get_db),
):

    return DashboardService.get_availability(db)


@router.get(
    "/doctors",
    response_model=DoctorListResponse,
)
def dashboard_doctors(
    db: Session = Depends(get_db),
):

    return DashboardService.get_doctors(db)


@router.get(
    "/patients",
    response_model=PatientListResponse,
)
def dashboard_patients(
    db: Session = Depends(get_db),
):

    return DashboardService.get_patients(db)