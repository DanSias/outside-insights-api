import logging
import sys
from pathlib import Path

# Logging Configuration
LOG_LEVEL = logging.DEBUG  # Change to logging.INFO in production
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_FILE = Path("logs/app.log")


def setup_logger():
    """Configures application-wide logging."""

    # Ensure logs directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(LOG_LEVEL)

    # Create formatter and add to handlers
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Get root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent double logging issue
    logger.propagate = False


setup_logger()
logger = logging.getLogger("ai-api-backend")

logger.info("Logging system initialized successfully.")
