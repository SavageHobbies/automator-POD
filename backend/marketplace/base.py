from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ProductImage(BaseModel):
    """Model for product images"""
    url: str
    position: Optional[int] = None
    is_default: bool = False

class ProductVariant(BaseModel):
    """Model for product variants"""
    title: str
    price: float
    sku: Optional[str] = None
    is_enabled: bool = True

class ProductData(BaseModel):
    """Model for product data"""
    title: str
    description: str
    images: List[ProductImage]
    variants: List[ProductVariant]
    tags: List[str] = []

class MarketplaceBase(ABC):
    """Abstract base class for marketplace integrations."""

    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the marketplace."""
        pass

    @abstractmethod
    async def create_product(self, product_data: ProductData) -> str:
        """Create a new product in the marketplace.

        Args:
            product_data: Product information including images and variants

        Returns:
            str: The ID of the created product
        """
        pass

    @abstractmethod
    async def upload_image(self, image_path: str) -> ProductImage:
        """Upload an image to the marketplace.

        Args:
            image_path: Local path to the image file

        Returns:
            ProductImage: The uploaded image information
        """
        pass

    @abstractmethod
    async def publish_product(self, product_id: str) -> bool:
        """Publish a product to make it live.

        Args:
            product_id: The ID of the product to publish

        Returns:
            bool: True if published successfully
        """
        pass

    @abstractmethod
    async def get_product_status(self, product_id: str) -> Dict[str, Any]:
        """Get the current status of a product.

        Args:
            product_id: The ID of the product to check

        Returns:
            Dict containing the product status information
        """
        pass