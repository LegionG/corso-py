from fastapi import FastAPI, HTTPException
import sqlite3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from init_db import dbInit   
from progetto_classi_validazione import router as prodotti_router
from progetto_utente import router as utenti_router

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- CORRETTO
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, PUT, DELETE ecc.
    allow_headers=["*"],   # tutti gli headers
)

app.include_router(prodotti_router)
app.include_router(utenti_router)

@app.get("/")
def home():
    return {"info": "Server principale attivo"}

dbInit()







