from fastapi import APIRouter
import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ProdottoIn(BaseModel):
    nome: str
    prezzo: float

class UtenteAuth(BaseModel):
    username: str
    password: str    

class FilmAuth(BaseModel):
	titolo: str
	trama: str
	anno: int
	url_locandina: str
	tmdb_id: str    

@router.get("/")
def root():
    return {"messaggio": "Benvenuto!"}

# Lista prodotti
@router.get("/prodotti")
def lista_prodotti():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

# Prodotto singolo
@router.get("/prodotti/{id_prodotto}")
def lista_prodotto_singolo(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone()
    conn.close()

    if risultato is None:
        raise HTTPException(status_code=404, detail="Prodotto non trovato")
    return risultato

# Creazione prodotto
@router.post("/prodotti", status_code=201)
def crea_prodotto(dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prodotti (nome, prezzo) VALUES (?, ?)",
        (dati.nome, dati.prezzo)
    )
    conn.commit()
    conn.close()
    return {"status": "Prodotto registrato con successo"}

# Aggiornamento prodotto
@router.put("/prodotti/{id_prodotto}")
def aggiorna_prodotto(id_prodotto: int, dati: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone()
    if risultato is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato")

    cursor.execute(
        "UPDATE prodotti SET nome = ?, prezzo = ? WHERE id = ?",
        (dati.nome, dati.prezzo, id_prodotto)
    )
    conn.commit()
    conn.close()
    return {"status": "Modifica salvata"}

# Eliminazione prodotto
@router.delete("/prodotti/{id_prodotto}")
def elimina(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prodotti WHERE id = ?", (id_prodotto,))
    risultato = cursor.fetchone()
    if risultato is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato")

    cursor.execute("DELETE FROM prodotti WHERE id = ?", (id_prodotto,))
    conn.commit()
    conn.close()
    return {"status": "Cancellato"}

