from fastapi import FastAPI
import sqlite3

app = FastAPI()


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
