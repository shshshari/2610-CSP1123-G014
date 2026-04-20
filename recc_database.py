import sqlite3

def init_db():
    conn = sqlite3.connect("stalls.db")
    cursor = conn.cursor()

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

    stalls_data = [
        ("Stall 1", "local",    "cheap",     "chill,filling",     "halal", "description."),
        ("Stall 2", "noodles",  "cheap",     "quick,filling",     "halal", "description."),
        ("Stall 3", "mamak",    "cheap",     "chaotic,filling",   "halal", "description."),
        ("Stall 4", "arab",     "cheap",     "smokey,filling",    "halal", "description."),
        ("Stall 5", "local",    "cheap",     "chill,filling",     "halal", "description."),
        ("Stall 6", "chinese",  "cheap",     "spicy,filling",     "halal", "description."),
        ("Stall 7", "local",    "cheap",     "explosive,filling", "halal", "description."),
        ("Stall 8", "mamak",    "cheap",     "diversity,filling", "halal", "description."),
        ("Stall 9", "korean",   "expensive", "quirky,filling",    "halal", "description."),
        ("Stall 10","cafe",     "cheap",     "calm,happy",        "halal", "description."),
    ]

    cursor.execute("SELECT COUNT(*) FROM stalls")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO stalls (name, category, price_range, vibe, dietary, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, stalls_data)

    conn.commit()
    conn.close()
    print("stalls.db created and ready!")

if __name__ == "__main__":
    init_db()
