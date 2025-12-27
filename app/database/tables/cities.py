def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        state_id INT NOT NULL,
        name VARCHAR(200) NOT NULL,
        FOREIGN KEY (state_id) REFERENCES states(id)
    );
    """)
