from sqlalchemy.orm import Session

from app.models import Doctor, Availability, Branch


def search_availability(
    db: Session,
    specialty=None,
    branch=None,
    date=None,
    preferred_time=None,
):
    query = (
        db.query(Availability, Doctor, Branch)
        .join(Doctor, Availability.doctor_id == Doctor.doctor_id)
        .filter(Availability.is_booked == False)
        .join(Branch, Doctor.branch_id == Branch.branch_id)
    )

    if specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))

    if branch:
        query = query.filter(Branch.name.ilike(f"%{branch}%"))

    if date:
        query = query.filter(Availability.date == date)

    if preferred_time:
        query = query.filter(Availability.start_time >= preferred_time)

    query = query.order_by(Availability.date, Availability.start_time)

    return query.limit(5).all()