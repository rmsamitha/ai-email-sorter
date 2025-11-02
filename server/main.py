from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

init_db()

app = FastAPI(title="AI Email Sorter API", version="1.0.0")

# Configure CORS
# Get allowed origins from environment variable or use defaults
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Email Sorter API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

