from fastapi import FastAPI
from instagrapi import Client
import os

app = FastAPI(title="Instagrapi API", version="1.0.0")

@app.get("/")
def root():
    return {"status": "ok", "message": "Instagrapi API running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
