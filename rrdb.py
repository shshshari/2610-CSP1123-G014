import sqlite3

def init_ratings_db():
    conn = sqlite3.connect("stalls.db")
    cursor = conn.cursor()

    # placeholder users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL
        )
    """)

    # ratings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stall_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stall_id) REFERENCES stalls(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(stall_id, user_id)
        )
    """)

    # reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stall_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stall_id) REFERENCES stalls(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(stall_id, user_id)
        )
    """)

    # placeholder users can delete later
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (username) VALUES (?)", [
            ("shari",),
            ("shinjie",),
            ("meera",),
        ])

    conn.commit()
    conn.close()
    print("ratings + reviews tables ready!")

if __name__ == "__main__":
    init_ratings_db()
