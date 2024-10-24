import os
import requests
from typing import Dict, Any

class MockupService:
    def __init__(self):
        self.api_key = os.getenv("DYNAMIC_MOCKUPS_API_KEY")
        self.base_url = "https://api.dynamicmockups.com/v1"
        
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_mockup(self, design_url: str, template: str = "product") -> Dict[str, Any]:
        """
        Generate a mockup using the Dynamic Mockups API
        """
        endpoint = f"{self.base_url}/mockups/generate"
        
        payload = {
            "template": template,
            "design": design_url
        }
        
        response = requests.post(
            endpoint,
            headers=self._get_headers(),
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
    
    async def get_templates(self) -> Dict[str, Any]:
        """
        Get available mockup templates
        """
        endpoint = f"{self.base_url}/templates"
        
        response = requests.get(
            endpoint,
            headers=self._get_headers()
        )
        
        response.raise_for_status()
        return response.json()

mockup_service = MockupService()