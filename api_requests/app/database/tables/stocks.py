from ..connection import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_id INT NOT NULL,
        exchange_id INT NOT NULL,
        symbol VARCHAR(20) NOT NULL,
        isin VARCHAR(20) UNIQUE,
        type ENUM('ON','PN','ETF','ADR','Other') DEFAULT 'ON',
        currency VARCHAR(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY idx_stock_company_exchange (company_id, exchange_id, symbol),
        FOREIGN KEY (company_id) REFERENCES companies(id),
        FOREIGN KEY (exchange_id) REFERENCES exchanges(id)
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
