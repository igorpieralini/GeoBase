from ..connection import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_indicators (
        id INT AUTO_INCREMENT PRIMARY KEY,
        stock_id INT NOT NULL,
        date DATE NOT NULL,
        pe_ratio DECIMAL(10,4),
        roe DECIMAL(10,4),
        debt_equity DECIMAL(10,4),
        market_cap BIGINT,
        beta DECIMAL(10,4),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY idx_stock_indicator (stock_id, date),
        FOREIGN KEY (stock_id) REFERENCES stocks(id)
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
