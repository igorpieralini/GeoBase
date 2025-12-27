import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.services.database_service import DatabaseService
from app.services.locales_service import LocalesService
from app.utils.config import load_config

def create_api():
    cfg = load_config()

    db_service = DatabaseService()
    db_service.initialize()

    locales_cfg = cfg.get('locales_import', {})
    if bool(locales_cfg.get('import_on_start', False)):
        locales_service = LocalesService()
        locales_service.run_import()

    return cfg, db_service
