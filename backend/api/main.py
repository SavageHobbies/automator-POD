"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.api.routes import designs, mockups, pod
import os

app = FastAPI(title="Design Generation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(designs.router, prefix="/api/designs", tags=["designs"])
app.include_router(mockups.router, prefix="/api/mockups", tags=["mockups"])
app.include_router(pod.router, prefix="/api/pod", tags=["pod"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}