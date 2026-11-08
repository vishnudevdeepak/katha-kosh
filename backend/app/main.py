"""
Kathā-Kosh FastAPI application entry point.
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app.routes import items, search, contributions, auth, regions, admin, ai

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kathā-Kosh API",
    description="API for Kathā-Kosh — India's Living Heritage Archive",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uploads static directory
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(items.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(contributions.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(regions.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(ai.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Kathā-Kosh API", "version": "1.0.0", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok"}
