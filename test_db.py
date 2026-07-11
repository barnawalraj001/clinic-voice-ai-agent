import logging

from app.database import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)

try:
    with engine.connect():
        logger.info("Database connected successfully")
except Exception:
    logger.exception("Database connection failed")