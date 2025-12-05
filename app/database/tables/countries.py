def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS countries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        code CHAR(2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
