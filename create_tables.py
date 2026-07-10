from app.database import Base, engine
from app.models import Branch, Doctor, Availability, Appointment

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")