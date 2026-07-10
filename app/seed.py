import csv

from app.database import SessionLocal
from app.models import Branch, Doctor
from app.services.availability_generator import generate_availability


def seed_branches():
    db = SessionLocal()

    with open("dataset/branches.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            branch = Branch(
                branch_id=row["branch_id"],
                name=row["name"],
                address=row["address"],
                city=row["city"],
                state=row["state"],
            )

            db.merge(branch)

    db.commit()
    db.close()


def seed_doctors():
    db = SessionLocal()

    with open("dataset/doctors.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            doctor = Doctor(
                doctor_id=row["doctor_id"],
                name=row["name"],
                specialty=row["specialty"],
                branch_id=row["branch_id"],
                experience_years=int(row["experience_years"]),
            )

            db.merge(doctor)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed_branches()
    seed_doctors()
    generate_availability()

    print("✅ Database Seeded Successfully!")