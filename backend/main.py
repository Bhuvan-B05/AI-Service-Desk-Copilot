from fastapi import FastAPI
from sqlalchemy import text
from database import Base, engine
import models
from database import engine
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Service Desk Copilot API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-service-desk-copilot-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

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