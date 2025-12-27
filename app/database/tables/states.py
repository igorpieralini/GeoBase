def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS states (
        id INT AUTO_INCREMENT PRIMARY KEY,
        country_id INT NOT NULL,
        name VARCHAR(200) NOT NULL,
        code VARCHAR(20),
        FOREIGN KEY (country_id) REFERENCES countries(id)
    );
    """)
