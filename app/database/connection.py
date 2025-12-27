import mysql.connector
from app.utils.config import load_config

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
