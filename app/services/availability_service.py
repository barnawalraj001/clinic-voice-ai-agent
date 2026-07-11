from sqlalchemy.orm import Session

from app.models import Doctor, Availability, Branch

BRANCH_ALIASES = {
    "em bypass": "B001",
    "apollo em bypass": "B001",
    "apollo multispeciality hospitals em bypass": "B001",
    "apollo multispeciality hospitals em bypass, kolkata": "B001",

    "narendrapur": "B002",
    "apollo hospitals narendrapur": "B002",
}

SPECIALTY_ALIASES = {
    "cardiologist": "Cardiology",
    "cardiology": "Cardiology",

    "orthopedic": "Orthopedics",
    "orthopedist": "Orthopedics",
    "orthopaedic": "Orthopedics",
    "orthopedics": "Orthopedics",

    "pediatrician": "Pediatrics",
    "pediatrics": "Pediatrics",

    "gynecologist": "Obstetrics & Gynecology",
    "gynaecologist": "Obstetrics & Gynecology",
    "obgyn": "Obstetrics & Gynecology",
    "obstetrics": "Obstetrics & Gynecology",

    "gastroenterologist": "Gastroenterology & Hepatology",
    "gastroenterology": "Gastroenterology & Hepatology",
    "hepatology": "Gastroenterology & Hepatology",
}


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
        specialty_lower = specialty.lower().strip()

        normalized_specialty = None

        for alias, canonical in SPECIALTY_ALIASES.items():
            if alias in specialty_lower:
                normalized_specialty = canonical
                break

        if normalized_specialty:
            specialty = normalized_specialty

        query = query.filter(
            Doctor.specialty.ilike(f"%{specialty}%")
        )

    if branch:
        branch_lower = branch.lower().strip()

        matched_branch_id = None

        for alias, branch_id in BRANCH_ALIASES.items():
            if alias in branch_lower:
                matched_branch_id = branch_id
                break

        if matched_branch_id:
            query = query.filter(
                Branch.branch_id == matched_branch_id
            )
        else:
            query = query.filter(
                Branch.name.ilike(f"%{branch}%")
            )

    if date:
        query = query.filter(Availability.date == date)

    if preferred_time:
        query = query.filter(Availability.start_time >= preferred_time)

    query = query.order_by(Availability.date, Availability.start_time)

    return query.limit(5).all()