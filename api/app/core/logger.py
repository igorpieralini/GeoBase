import os
import logging
from app.config import settings

if settings.logging.save_to_file and settings.logging.file_path:
    os.makedirs(os.path.dirname(settings.logging.file_path), exist_ok=True)

logger = logging.getLogger("finance_ai")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if settings.logging.save_to_file and settings.logging.file_path:
    file_handler = logging.FileHandler(settings.logging.file_path)
    file_handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    logger.addHandler(console_handler)
