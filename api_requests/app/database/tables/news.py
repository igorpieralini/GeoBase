from ..connection import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_id INT NOT NULL,
        stock_id INT,
        title VARCHAR(500),
        description TEXT,
        content LONGTEXT,
        url VARCHAR(500),
        published_at DATETIME,
        source_id INT,
        sentiment ENUM('positive','negative','neutral') DEFAULT 'neutral',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (company_id) REFERENCES companies(id),
        FOREIGN KEY (stock_id) REFERENCES stocks(id)
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
