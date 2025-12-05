from app.utils.logger import log_message
from app.database.queries.locales.locales_update_query import import_all_locations

class LocalesService:

    def run_import(self):
        log_message("Iniciando serviço de importação de localidades...", level="INFO")
        import_all_locations()
        log_message("Serviço de importação concluído.", level="INFO")
