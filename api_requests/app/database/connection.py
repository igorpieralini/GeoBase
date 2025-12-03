import mysql.connector
from mysql.connector import errorcode
from app.utils.config import cfg
from app.utils.logger import log_message

db_config = cfg['database']

def get_connection(create_db=False):
    try:
        log_message("Iniciando processo de conexão com o banco de dados...", level="INFO")
        params = {
            "host": db_config['host'],
            "user": db_config['user'],
            "password": db_config['password']
        }
        log_message(f"Parâmetros de conexão: host={params['host']}, user={params['user']}", level="DEBUG")
        if not create_db:
            params["database"] = db_config['database']
            log_message(f"Conectando ao banco de dados: {db_config['database']}", level="INFO")
        else:
            log_message("Conectando sem especificar banco de dados (para criação)", level="INFO")
        conn = mysql.connector.connect(**params)
        log_message("Conexão com o MySQL estabelecida com sucesso.", level="INFO")
        return conn
    except mysql.connector.Error as err:
        log_message(f"Erro ao conectar ao banco de dados: {err}", level="ERROR")
        raise
