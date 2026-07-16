from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from init_db_progetto import dbInit
from progetto_film import router as film_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(film_router)

@app.get("/")
def home():
    return {"info": "Cinemaniaci"}

dbInit()