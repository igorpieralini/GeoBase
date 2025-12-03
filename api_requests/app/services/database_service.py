from app.database.connection import get_connection
from app.database.create_database import create_database, create_tables
from app.utils.logger import log_message

class DatabaseService:
    def __init__(self):
        self.conn = None

    def initialize(self):
        try:
            # Step 1: Connect to MySQL without specifying DB
            self.conn = get_connection(create_db=True)
            log_message("Connected to MySQL successfully.", level="INFO")

            # Step 2: Create the database
            create_database()
            log_message("Database created ou já existe.", level="INFO")

            # Step 3: Create all tables
            create_tables()
            log_message("Todas as tabelas criadas com sucesso.", level="INFO")

        except Exception as e:
            log_message(f"Erro ao inicializar o banco de dados: {e}", level="ERROR")
            raise
        finally:
            if self.conn:
                self.conn.close()
                log_message("Conexão MySQL encerrada após inicialização.", level="INFO")
