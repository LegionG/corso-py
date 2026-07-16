from fastapi import FastAPI, APIRouter, HTTPException
import sqlite3

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
def cerca_film(keyword: str):
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM film WHERE titolo LIKE ?", 
        (f"%{keyword}%",)
    )

    risultato = cursor.fetchall()
    conn.close()
    if risultato==None:
        raise HTTPException(status_code=400, detail="Film non trovato")

    return [dict(r) for r in risultato]

@router.get("/film/{id}")
def cerca_film(id: int):
    conn = sqlite3.connect("database_progetto.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM film WHERE id LIKE ?", 
        (id,)
    )

    risultato = cursor.fetchall()
    conn.close()
    if risultato==None:
        raise HTTPException(status_code=400, detail="Film non trovato")

    return [dict(r) for r in risultato]
    