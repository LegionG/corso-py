# corso-py

Piccolo progetto di esercizio per imparare Python, usato come corso introduttivo.
Include esercizi base (`prova.py`, `registro.py`), lavoro con JSON (`api_data.py`)
e una piccola API con FastAPI + SQLite (`main.py`, `init_db.py`).

## Setup

```bash
pip install -r requirements.txt
```

## Inizializzare il database

```bash
python init_db.py
```

Crea (o svuota e ripopola) `database.db` con una tabella `prodotti` di esempio.

## Avviare l'API

```bash
python main.py
```

oppure

```bash
uvicorn main:app --reload
```

L'API sara' disponibile su `http://127.0.0.1:8000`.

### Endpoint disponibili

- `GET /prodotti/cerca?keyword=...` — cerca i prodotti il cui nome contiene la keyword

## File di esercizio

- `prova.py` — funzioni base (somma, sottrazione, moltiplicazione, radice quadrata)
- `registro.py` — esempio di lista e ciclo `for`
- `api_data.py` — esempio di parsing JSON
