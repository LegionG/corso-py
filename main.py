from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# @app.get("/calcola")
# def root(num1: int = 1, num2: int = 1, operazione: str = "somma"):

#     if (num1 == 1 and num2 == 1):
#         raise HTTPException(status_code=400, detail="Operazione non valida")

#     match operazione:
#         case "somma":
#             return {"Il risultato della somma e'": num1 + num2}
#         case "sottrazione":
#             return {"Il risultato della sottrazione e'": num1 - num2}
#         case "moltiplicazione":
#             return {"Il risultato della moltiplicazione e'": num1 * num2}
#         case _:
#             raise HTTPException(status_code=400, detail="Operazione non valida")

# @app.get("/prodotti")
# def ottideni_prodotti():
#     conn = sqlite3.connect("database.db")
#     conn.row_factory = sqlite3.Row 
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM prodotti")
#     risultato = cursor.fetchall()
#     conn.close()
#     return risultato

@app.get("/prodotti/cerca")
def cerca_prodotti(keyword:str):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti WHERE nome LIKE ?", (f"%{keyword}%",))
    risultato = cursor.fetchall()
    conn.close()
    return risultato