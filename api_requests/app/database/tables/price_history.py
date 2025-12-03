from ..connection import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        stock_id INT NOT NULL,
        date DATE NOT NULL,
        open DECIMAL(15,4),
        high DECIMAL(15,4),
        low DECIMAL(15,4),
        close DECIMAL(15,4),
        volume BIGINT,
        adjusted_close DECIMAL(15,4),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY idx_stock_date (stock_id, date),
        FOREIGN KEY (stock_id) REFERENCES stocks(id)
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
