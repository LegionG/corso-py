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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titolo_playlist TEXT NOT NULL,
            data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_film (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id INTEGER NOT NULL,
            film_id INTEGER NOT NULL,
            FOREIGN KEY (playlist_id) REFERENCES playlist (id),
            FOREIGN KEY (film_id) REFERENCES film (id)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM film")

    if cursor.fetchone()[0] == 0:
        film_esempi = [
            ("Inception", "Un ladro che ruba segreti aziendali attraverso i sogni", 2010, "https://image.tmdb.org/t/p/w500/5QHWgqaBxZI1eM5e3YhyKzY5o3z.jpg", "27205"),
            ("The Matrix", "Un hacker scopre la vera natura della realtà", 1999, "https://image.tmdb.org/t/p/w500/yQZX4scmfYtj4ccKFNGZJlOj1y9.jpg", "603"),
            ("Interstellar", "Un gruppo di astronauti viaggia attraverso un wormhole", 2014, "https://image.tmdb.org/t/p/w500/bMKiLh0mES4Uiococ240lbbTGXQ.jpg", "157336"),
            ("The Dark Knight", "Batman affronta il Joker che semina il caos", 2008, "https://image.tmdb.org/t/p/w500/1hRoyzDtpgMU7Dz4IEIga7AWP4b.jpg", "155"),
            ("Pulp Fiction", "Quattro storie di violenza e redenzione", 1994, "https://image.tmdb.org/t/p/w500/d5iIlVn42g9dKSz5rt7c0D2yvDJ.jpg", "680"),
            ("Forrest Gump", "Un uomo di intelligenza limitata testimone della storia americana", 1994, "https://image.tmdb.org/t/p/w500/arw3EN9pWJt1PsJpie3bCn4Yo2d.jpg", "13"),
            ("The Shawshank Redemption", "Due uomini nella prigione formano un legame duraturos", 1994, "https://image.tmdb.org/t/p/w500/q6y0Go1TSiQPnBAK_RA7CiDBi1b.jpg", "278"),
            ("Titanic", "Un amore tra le classi sociali sul Titanic", 1997, "https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOG8.jpg", "597"),
            ("Avatar", "Un marine combatte per proteggere Pandora", 2009, "https://image.tmdb.org/t/p/w500/jRXYj3sqQPRdSKl2IR7S25vDdar.jpg", "19995"),
            ("Gladiator", "Un generale romano torna come gladiatore", 2000, "https://image.tmdb.org/t/p/w500/P2fLc9n3dVrKW4zYrKWT7nEKPZI.jpg", "98"),
            ("Il Signore degli Anelli - La Comunità dell'Anello", "Una compagnia si unisce per distruggere l'Anello del Potere", 2001, "https://image.tmdb.org/t/p/w500/5VTN0pR8gcqV0gZeSEFLdBFaGLF.jpg", "120"),
            ("Avengers: Endgame", "Gli Avengers si riuniscono per affrontare Thanos", 2019, "https://image.tmdb.org/t/p/w500/or06FQrDKlPKOQ6W9CdqHLEvCAl.jpg", "299534"),
            ("Parasite", "Una famiglia povera infiltra una ricca casa", 2019, "https://image.tmdb.org/t/p/w500/sy6DvMECF2CD6NtRZgW7gI8o0BS.jpg", "496243"),
            ("Oppenheimer", "La storia del padre della bomba atomica", 2023, "https://image.tmdb.org/t/p/w500/8Gxv8gSZDMIA_AEg7kIJMXar0Ey.jpg", "872585"),
            ("Dune", "Adattamento del capolavoro di fantascienza", 2021, "https://image.tmdb.org/t/p/w500/n6bUvigpRFqSwmPp1vMtR6th6gg.jpg", "438631"),
            ("Joker", "L'ascesa psicologica di un uomo verso la follia", 2019, "https://image.tmdb.org/t/p/w500/udDclJoHjfjb3fUVU5pwc6OWeWS.jpg", "475557"),
            ("The Godfather", "La saga della famiglia Corleone", 1972, "https://image.tmdb.org/t/p/w500/rPdtLWNsZmAtoZl9PK7SXZK7Fia.jpg", "238"),
            ("Inception", "Heist nel mondo dei sogni", 2010, "https://image.tmdb.org/t/p/w500/9gk7adHYeDMNNGceKc06f6I9xvA.jpg", "27205"),
            ("Tenet", "Un'operazione attraverso il tempo", 2020, "https://image.tmdb.org/t/p/w500/ucS3wFjWChYcBNAb9kxX8ZYl9j8.jpg", "577922"),
            ("Inception", "Sogni dentro sogni", 2010, "https://image.tmdb.org/t/p/w500/1p0Cfp7Due021me67VP4a6i2wSb.jpg", "27205"),
        ]

        cursor.executemany("""
            INSERT INTO film (titolo, trama, anno, url_locandina, tmdb_id) 
            VALUES (?, ?, ?, ?, ?)
        """, film_esempi)

        conn.commit()

    conn.close()