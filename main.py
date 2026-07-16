from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()


class ProdottoIn(BaseModel):
    nome: str
    prezzo: float


@app.get("/prodotti")
def ottieni_prodotti():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato


@app.get("/prodotti/cerca")
def cerca_prodotti(keyword: str):
    """Cerca i prodotti nel database il cui nome contiene la keyword passata."""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti WHERE nome LIKE ?", (f"%{keyword}%",))
    risultato = cursor.fetchall()
    conn.close()
    return risultato


@app.delete("/prodotti/cancella/{id_prodotto}")
def elimina(id_prodotto: int):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM prodotti WHERE id = ?", (id_prodotto,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato")

    conn.close()
    return {"messaggio": "Prodotto eliminato"}


@app.put("/prodotti/modifica/{id_prodotto}")
def aggiorna(id_prodotto: int, prodottoIn: ProdottoIn):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE prodotti SET nome = ?, prezzo = ? WHERE id = ?",
        (prodottoIn.nome, prodottoIn.prezzo, id_prodotto)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Prodotto non trovato")

    conn.close()
    return {"messaggio": "Prodotto aggiornato"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)