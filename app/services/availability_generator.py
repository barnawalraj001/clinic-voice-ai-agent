import logging
import random
from datetime import date, timedelta, time

from app.database import SessionLocal
from app.models import Doctor, Availability

logger = logging.getLogger(__name__)


def generate_availability(days=30):

    db = SessionLocal()

    # Remove old availability so rerunning doesn't create duplicates
    db.query(Availability).delete()

    doctors = db.query(Doctor).all()

    today = date.today()

    for doctor in doctors:

        for day in range(days):

            current_date = today + timedelta(days=day)

            # Skip Sunday
            if current_date.weekday() == 6:
                continue

            current_time = time(9, 0)

            while current_time < time(17, 0):

                # Lunch break
                if time(13, 0) <= current_time < time(14, 0):
                    current_time = time(14, 0)
                    continue

                hour = current_time.hour
                minute = current_time.minute

                if minute == 30:
                    end_time = time(hour + 1, 0) if hour < 23 else time(23, 59)
                else:
                    end_time = time(hour, 30)

                slot = Availability(
                    doctor_id=doctor.doctor_id,
                    date=current_date,
                    start_time=current_time,
                    end_time=end_time,
                    is_booked=random.random() < 0.2
                )

                db.add(slot)

                current_time = end_time

    db.commit()
    db.close()

    logger.info("Availability generated")