from .connection import get_connection
from app.utils.logger import log_message
from app.utils.config import cfg

def create_database():
    conn = get_connection(create_db=True)
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cfg['database']['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        log_message("Database created or already exists.", level="INFO")
    except Exception as e:
        log_message(f"Error creating database: {e}", level="ERROR")
        raise
    finally:
        cursor.close()
        conn.close()

def create_tables():
    from .tables import countries, states, cities, exchanges, companies, stocks, price_history, news, financial_indicators

    countries.create_table()
    states.create_table()
    cities.create_table()
    exchanges.create_table()
    companies.create_table()
    stocks.create_table()
    price_history.create_table()
    news.create_table()
    financial_indicators.create_table()

if __name__ == "__main__":
    create_database()
    create_tables()
    print("Database and all tables created successfully.")
