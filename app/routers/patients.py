from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.patient import (
    SearchPatientRequest,
    SearchPatientResponse,
)

from app.services.patient_service import PatientService

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post(
    "/search",
    response_model=SearchPatientResponse,
)
def search_patient(
    request: SearchPatientRequest,
    db: Session = Depends(get_db),
):

    return PatientService.search_patient(
        db=db,
        phone=request.phone,
    )