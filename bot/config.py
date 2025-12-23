import datetime
import logging

# Channel / scheduling
VOCAB_DAILY_CHANNEL = "vocab-daily"
TIME_TO_POST = datetime.time(hour=23, minute=10, second=0)  # midnight UTC

# LLM / prompt settings
MODEL_ID = "gemini-flash-latest"
ACTIVE_VOCAB_CHANNEL = "active-vocab-inbox"

# Logging configuration
# Call `configure_logging()` once at application startup (for example in `main.py`).
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

def configure_logging(level: int = LOG_LEVEL, fmt: str = LOG_FORMAT):
	"""Configure the root logger for the application.

	Example in `main.py`:
		from bot.config import configure_logging
		configure_logging()
	"""
	logging.basicConfig(level=level, format=fmt)
