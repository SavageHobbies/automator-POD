from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from backend.api.services.mockup_service import mockup_service

router = APIRouter()

@router.post("/generate")
async def generate_mockup(data: Dict[str, Any]):
    try:
        design_data = data.get("designData", {})
        design_url = design_data.get("imageUrl")
        
        if not design_url:
            raise HTTPException(status_code=400, detail="Design URL is required")
        
        # Generate mockup using Dynamic Mockups API
        mockup_result = await mockup_service.generate_mockup(design_url)
        
        return {
            "success": True,
            "mockup": mockup_result,
            "designData": design_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_templates():
    try:
        templates = await mockup_service.get_templates()
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))