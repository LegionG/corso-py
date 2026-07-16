from fastapi import FastAPI, APIRouter, HTTPException
import sqlite3
from progetto_classi_validazione import FilmAuth

router = APIRouter()

@router.get("/film")
def get_film():
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM film")
    rows = cursor.fetchall()

    conn.close()
    return [dict(r) for r in rows]


@router.get("/film/cerca")
def cerca_film_per_titolo(keyword: str):
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM film WHERE titolo LIKE ?", 
        (f"%{keyword}%",)
    )

    risultato = cursor.fetchall()
    conn.close()

    return [dict(r) for r in risultato]


@router.get("/film/{id}")
def cerca_film_per_id(id: int):
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM film WHERE id = ?", 
        (id,)
    )

    risultato = cursor.fetchall()
    conn.close()
    if not risultato:
        raise HTTPException(status_code=404, detail="Film non trovato")

    return [dict(r) for r in risultato]


@router.post("/film/aggiungi")
def aggiungi_film(dati: FilmAuth):
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO film (titolo, trama, anno, url_locandina, tmdb_id) VALUES (?, ?, ?, ?, ?)",
        (dati.titolo, dati.trama, dati.anno, dati.url_locandina, dati.tmdb_id)
    )
    conn.commit()
    film_id = cursor.lastrowid
    conn.close()

    return {"id": film_id, "status": "Film aggiunto"}


# ===== ENDPOINT PER VIDEO =====

@router.get("/film/{id}/video")
def get_video_film(id: int):
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM elementi_video WHERE film_id = ?", (id,))
    risultato = cursor.fetchall()
    conn.close()

    return [dict(r) for r in risultato]


@router.post("/film/{id}/video")
def aggiungi_video(id: int, dati: dict):
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    # Verifica che il film esista
    cursor.execute("SELECT id FROM film WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Film non trovato")

    cursor.execute(
        "INSERT INTO elementi_video (film_id, url_video_youtube, commento) VALUES (?, ?, ?)",
        (id, dati["url_video_youtube"], dati.get("commento", ""))
    )
    conn.commit()
    conn.close()

    return {"status": "Video aggiunto"}


@router.delete("/film/{id}/video/{video_id}")
def elimina_video(id: int, video_id: int):
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    # Verifica che il video appartenga al film
    cursor.execute("SELECT id FROM elementi_video WHERE id = ? AND film_id = ?", (video_id, id))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Video non trovato")

    cursor.execute("DELETE FROM elementi_video WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()

    return {"status": "Video eliminato"}


# ===== ENDPOINT PER PLAYLIST =====

@router.get("/playlist")
def get_playlist():
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM playlist")
    risultato = cursor.fetchall()
    conn.close()

    return [dict(r) for r in risultato]


@router.post("/playlist")
def crea_playlist(dati: dict):
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO playlist (titolo_playlist) VALUES (?)",
        (dati["titolo_playlist"],)
    )
    conn.commit()
    playlist_id = cursor.lastrowid
    conn.close()

    return {"id": playlist_id, "status": "Playlist creata"}


@router.delete("/playlist/{id}")
def elimina_playlist(id: int):
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    # Verifica che la playlist esista
    cursor.execute("SELECT id FROM playlist WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Playlist non trovata")

    # Elimina i film dalla playlist
    cursor.execute("DELETE FROM playlist_film WHERE playlist_id = ?", (id,))
    
    # Elimina la playlist
    cursor.execute("DELETE FROM playlist WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"status": "Playlist eliminata"}


@router.get("/playlist/{id}/film")
def get_film_playlist(id: int):
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.id as film_id, f.titolo, f.trama, f.anno, f.url_locandina, f.tmdb_id
        FROM film f
        JOIN playlist_film pf ON f.id = pf.film_id
        WHERE pf.playlist_id = ?
    """, (id,))
    
    risultato = cursor.fetchall()
    conn.close()

    return [dict(r) for r in risultato]


@router.post("/playlist/{id}/film")
def aggiungi_film_playlist(id: int, dati: dict):
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    # Verifica che la playlist esista
    cursor.execute("SELECT id FROM playlist WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Playlist non trovata")

    # Verifica che il film esista
    cursor.execute("SELECT id FROM film WHERE id = ?", (dati["film_id"],))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Film non trovato")

    # Verifica che il film non sia già nella playlist
    cursor.execute("SELECT id FROM playlist_film WHERE playlist_id = ? AND film_id = ?", (id, dati["film_id"]))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Film già in questa playlist")

    cursor.execute(
        "INSERT INTO playlist_film (playlist_id, film_id) VALUES (?, ?)",
        (id, dati["film_id"])
    )
    conn.commit()
    conn.close()

    return {"status": "Film aggiunto alla playlist"}


@router.delete("/playlist/{id}/film/{film_id}")
def rimuovi_film_playlist(id: int, film_id: int):
    conn = sqlite3.connect("database_progetto.db")
    cursor = conn.cursor()

    # Verifica che la relazione esista
    cursor.execute("SELECT id FROM playlist_film WHERE playlist_id = ? AND film_id = ?", (id, film_id))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Film non trovato in questa playlist")

    cursor.execute("DELETE FROM playlist_film WHERE playlist_id = ? AND film_id = ?", (id, film_id))
    conn.commit()
    conn.close()

    return {"status": "Film rimosso dalla playlist"}