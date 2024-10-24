# backend/core/product_service.py
from typing import List, Dict, Any
from ..marketplace.base import MarketplaceBase
from ..marketplace.printify import PrintifyMarketplace

class ProductService:
    def __init__(self):
        self.marketplace: MarketplaceBase = PrintifyMarketplace()

    async def create_and_publish_product(self, 
                                       design_data: Dict[str, Any],
                                       mockup_paths: List[str]) -> Dict[str, Any]:
        """Create and publish a product with its designs and mockups."""
        try:
            # Upload images to marketplace
            image_ids = []
            for mockup_path in mockup_paths:
                image_id = await self.marketplace.upload_image(mockup_path)
                image_ids.append(image_id)

            # Create product with uploaded images
            product_data = {
                "title": design_data["title"],
                "description": design_data["description"],
                "images": image_ids,
                # Add other required product data
            }

            # Create product in marketplace
            product_id = await self.marketplace.create_product(product_data)

            # Publish product
            success = await self.marketplace.publish_product(product_id)

            return {
                "success": success,
                "product_id": product_id,
                "image_ids": image_ids
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }