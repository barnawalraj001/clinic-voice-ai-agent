import logging

from app.database import Base, engine
from app.models import Branch, Doctor, Availability, Appointment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

logger.info("Tables created successfully")