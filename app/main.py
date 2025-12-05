import sys
from pathlib import Path
import os
import time

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.services.database_service import DatabaseService
from app.services.locales_service import LocalesService
from app.utils.config import load_config
from app.utils.logger import log_message

def create_api(fetch_news_on_start: bool | None = None):
    start_time = time.time()
    
    log_message("🚀 Iniciando aplicação...", level="INFO")

    cfg = load_config()

    log_path = cfg.get('logging', {}).get('path', 'logs/')
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)
        log_message(f"📁 Pasta de logs criada em: {log_path}", level="SUCCESS")

    db_service = DatabaseService()
    try:
        db_service.initialize()
    except Exception as e:
        log_message(f"Erro inicializando DatabaseService: {e}", level="ERROR")
        raise

    locales_cfg = cfg.get('locales_import', {})
    if bool(locales_cfg.get('import_on_start', False)):
        try:
            locales_service = LocalesService()
            locales_service.run_import()
        except Exception as e:
            log_message(f"Importação de localidades falhou: {e}", level="ERROR")

    elapsed_time = time.time() - start_time
    log_message(f"✨ Aplicação inicializada com sucesso em {elapsed_time:.2f}s!", level="SUCCESS")
    return cfg, db_service
