import sqlite3

def dbInit():
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS film (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titolo TEXT NOT NULL,
            trama TEXT,
            anno INTEGER,
            url_locandina TEXT,
            tmdb_id TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS elementi_video (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            film_id INTEGER NOT NULL,
            url_video_youtube TEXT NOT NULL,
            commento TEXT,
            FOREIGN KEY (film_id) REFERENCES film (id)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM film")

    if cursor.fetchone()[0] == 0:
        film_esempi = [
            ("Inception", "Un ladro che ruba segreti aziendali...", 2010, "https://image.tmdb.org/t/p/w500/5QHWgqaBxZI1eM5e3YhyKzY5o3z.jpg", "27205"),
            ("The Matrix", "Un hacker scopre la realtà...", 1999, "https://image.tmdb.org/t/p/w500/yQZX4scmfYtj4ccKFNGZJlOj1y9.jpg", "603"),
            ("Interstellar", "Viaggio nello spazio...", 2014, "https://image.tmdb.org/t/p/w500/bMKiLh0mES4Uiococ240lbbTGXQ.jpg", "157336")
        ]

        cursor.executemany("""
            INSERT INTO film (titolo, trama, anno, url_locandina, tmdb_id) 
            VALUES (?, ?, ?, ?, ?)
        """, film_esempi)

        conn.commit()

    conn.close()