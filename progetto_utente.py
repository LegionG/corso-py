from fastapi import FastAPI, APIRouter, HTTPException
import hashlib
import sqlite3
import secrets
from progetto_classi_validazione import UtenteAuth

app = FastAPI()
router = APIRouter()

@app.get("/")
def root():
    return {"message": "Hello World"}


def calcola_hash(password_chiaro: str):
    return hashlib.sha256(password_chiaro.encode('utf-8')).hexdigest()


@router.post("/registrazione")
def registrazione(dati: UtenteAuth):
    hash = calcola_hash(dati.password)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO utenti(username, password_hash) VALUES (?, ?)",
            (dati.username, hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username già esistente")

    conn.close()
    return {"status": "Utente registrato con successo"}


@router.post("/login")
def login(dati: UtenteAuth):
    hash = calcola_hash(dati.password)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM utenti WHERE username = ?",
        (dati.username,)
    )
    utente = cursor.fetchone()

    if utente is None or hash != utente[1]:
        conn.close()
        raise HTTPException(status_code=401, detail="Credenziali errate")

    username = utente[0]
    token_sessione = secrets.token_hex(16)

    cursor.execute(
        "UPDATE utenti SET token = ? WHERE id = ?",
        (token_sessione, username)
    )
    conn.commit()
    conn.close()

    return {
        "status": "Login riuscito",
        "token": token_sessione
    }

@router.get("/profilo")
def trovatratoken(token:str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()
    if utente is None:
        raise HTTPException(status_code=401, detail="Pass non valido!")
    conn.commit()
    conn.close()
    id_utente_reale = utente[0] 
    return id_utente_reale 