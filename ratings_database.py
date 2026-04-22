import sqlite3

def init_ratings_db():
    conn = sqlite3.connect("stalls.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stall_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stall_id) REFERENCES stalls(id),
            UNIQUE(stall_id, user_id)
        )
    """)

    conn.commit()
    conn.close()
    print("ratings table ready!")

if __name__ == "__main__":
    init_ratings_db()
