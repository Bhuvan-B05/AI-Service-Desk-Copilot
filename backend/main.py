from fastapi import FastAPI
from sqlalchemy import text

from database import engine

app = FastAPI(
    title="AI Service Desk Copilot API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Service Desk Copilot API is running 🚀"
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "database": str(e)
        }