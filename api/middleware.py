# api/middleware.py
from slowapi import Limiter
import logging
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)