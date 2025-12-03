from ..connection import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        sector VARCHAR(100),
        industry VARCHAR(100),
        country_id INT,
        state_id INT,
        city_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (country_id) REFERENCES countries(id),
        FOREIGN KEY (state_id) REFERENCES states(id),
        FOREIGN KEY (city_id) REFERENCES cities(id)
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
