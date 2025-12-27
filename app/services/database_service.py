import mysql.connector
from app.utils.config import load_config
from app.database.tables.countries import create_table as create_countries_table
from app.database.tables.states import create_table as create_states_table
from app.database.tables.cities import create_table as create_cities_table

def get_connection(database: str = None):
    """Cria e retorna uma conexão com o banco de dados."""
    
    config = load_config()
    db_config = config.get('database', {})
    
    try:
        conn = mysql.connector.connect(
            host=db_config.get('host', 'localhost'),
            user=db_config.get('user', 'root'),
            password=db_config.get('password', ''),
            database=database or db_config.get('database', 'traderia'),
            port=db_config.get('port', 3306)
        )
        return conn
    except mysql.connector.Error as e:
        raise

def create_database_if_not_exists():
    """Cria o banco de dados se não existir."""

    config = load_config()
    db_config = config.get('database', {})
    db_name = db_config.get('database', 'traderia')
    
    try:
    
        conn = mysql.connector.connect(
            host=db_config.get('host', 'localhost'),
            user=db_config.get('user', 'root'),
            password=db_config.get('password', ''),
            port=db_config.get('port', 3306)
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.commit()
        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        raise

class DatabaseService:
    """Serviço de gerenciamento do banco de dados."""
    
    def __init__(self):
        self.conn = None
    
    def initialize(self):
        """Inicializa o banco de dados e cria as tabelas se necessário."""

        try:
            create_database_if_not_exists()
            
            self.conn = get_connection()
            cursor = self.conn.cursor()
            
            create_countries_table(cursor)
            create_states_table(cursor)
            create_cities_table(cursor)
            
            self.conn.commit()
            cursor.close()
        except Exception as e:
            raise
    
    def get_connection(self):
        """Retorna a conexão atual."""

        if not self.conn:
            self.conn = get_connection()
        return self.conn
    
    def close(self):
        """Fecha a conexão com o banco de dados."""

        if self.conn:
            self.conn.close()
