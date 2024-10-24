"""Routes for Pattern on Demand (POD) operations."""
from fastapi import APIRouter, HTTPException
from backend.api.services.pod_service import PodService
from res.models.requests import PatternRequest
from res.models.responses import PatternResponse
from res.models.tshirt import TshirtWithIds

router = APIRouter()
pod_service = PodService()

@router.get("/")
async def root():
    """Root endpoint for POD service."""
    return {"message": "Welcome to the Max POD API"}

@router.post("/process_patterns", response_model=PatternResponse)
async def process_patterns(request: PatternRequest):
    """Process patterns based on the provided request."""
    try:
        patterns = await pod_service.process_patterns_and_idea(
            request.patterns, 
            request.idea
        )

        response_patterns = []
        for pattern in patterns:
            response_patterns.append(TshirtWithIds(**pattern))

        return PatternResponse(
            message="Generated Patterns Successfully",
            patterns=response_patterns
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))