from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import product_pipeline
from backend.api.mockup_routes import router as mockup_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the original routes
app.include_router(mockup_router, prefix="/api")

# Original favicon route
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favi.ico")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include the process_patterns endpoint
@app.post("/process_patterns")
async def process_patterns(request: product_pipeline.PatternRequest):
    return product_pipeline.process_patterns(request)