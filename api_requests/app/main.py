import sys
from pathlib import Path

root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.services.database_service import DatabaseService
from app.services.locales_service import LocalesService
from app.utils.config import load_config

import os
from app.utils.logger import log_message

def create_api():
    cfg = load_config()

    # Cria a pasta de logs se não existir
    log_path = cfg.get('logging', {}).get('path', 'logs/')
    if not os.path.exists(log_path):
        os.makedirs(log_path)
        log_message(f"Pasta de logs criada em: {log_path}", level="INFO")

    db_service = DatabaseService()
    db_service.initialize()

    LocalesService().run_import()
    log_message("API project initialized successfully!", level="INFO")
    return cfg, db_service