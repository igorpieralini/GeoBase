from app.database.queries.locales.locales_update_query import import_all_locations

class LocalesService:

    def run_import(self):
        import_all_locations()
