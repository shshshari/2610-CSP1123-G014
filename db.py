import sqlite3

def init_db():
    conn = sqlite3.connect("stalls.db")
    cursor = conn.cursor()

    # ======================
    # STALLS TABLE
    # ======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stalls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price_range TEXT NOT NULL,
        vibe TEXT NOT NULL,
        dietary TEXT NOT NULL,
        description TEXT NOT NULL
    )
    """)

    # ======================
    # USERS TABLE
    # ======================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL
    )
    """)

    # ======================
    # RATINGS TABLE
    # ======================
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

    # ======================
    # REVIEWS TABLE
    # ======================
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

    # ======================
    # FAVOURITES TABLE
    # ======================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stall_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stall_id) REFERENCES stalls(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(stall_id, user_id)
    )
    """)

    # ======================
    # SEED DATA (STALLS)
    # ======================
    cursor.execute("SELECT COUNT(*) FROM stalls")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO stalls (name, category, price_range, vibe, dietary, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("Stall 1", "local", "cheap", "chill,filling", "halal", "description."),
            ("Stall 2", "noodles", "cheap", "quick,filling", "halal", "description."),
            ("Stall 3", "mamak", "cheap", "chaotic,filling", "halal", "description."),
            ("Stall 4", "arab", "cheap", "smokey,filling", "halal", "description."),
            ("Stall 5", "local", "cheap", "chill,filling", "halal", "description."),
            ("Stall 6", "chinese", "cheap", "spicy,filling", "halal", "description."),
            ("Stall 7", "local", "cheap", "explosive,filling", "halal", "description."),
            ("Stall 8", "mamak", "cheap", "diversity,filling", "halal", "description."),
            ("Stall 9", "korean", "expensive", "quirky,filling", "halal", "description."),
            ("Stall 10", "cafe", "cheap", "calm,happy", "halal", "description.")
        ])

        # ======================
        # SEED DATA (USERS)
        # ======================
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (username) VALUES (?)", [
            ("shari",),
            ("shinjie",),
            ("meera",),
        ])

    conn.commit()
    conn.close()

    print("Full database ready!")

if __name__ == "__main__":
    init_db()