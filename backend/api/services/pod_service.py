"""Service for handling Pattern on Demand (POD) operations."""
import os
import random
import json
import uuid
from datetime import datetime
from urllib.parse import quote

from util.printify.printify_util import PrintifyUtil
from util.ai_util import AiUtil
from util.image_util import create_text_image
from util.github_util import GithubUploader
from res.models.tshirt import TshirtFromAiList
from res.prompts.tshirt import user_message, blueprint_6_description

class PodService:
    def __init__(self):
        random.seed(int(datetime.now().timestamp()))
        self.text_colors = [
            {"hex": "000000", "shade": "dark"},
            {"hex": "FFFFFF", "shade": "light"}
        ]
        self.ai = AiUtil()
        self.printify = PrintifyUtil()
        self.blueprint = 6  # Unisex Gildan T-Shirt
        self.printer = 99  # Printify Choice Provider

    async def process_patterns_and_idea(self, number_of_patterns: int, idea: str):
        variants, light_ids, dark_ids = self.printify.get_all_variants(
            self.blueprint, self.printer)
        
        # Apply the variant ids to the text colors
        for color in self.text_colors:
            if color.get("shade") == "light":
                color["variant_ids"] = dark_ids
            else:
                color["variant_ids"] = light_ids

        # Get patterns from AI
        response = self.ai.chat(
            messages=[
                {"role": "system", "content": "You are a helpful chatbot"},
                {"role": "user", "content": user_message %
                    (number_of_patterns, idea) + blueprint_6_description},
            ],
            output_model=TshirtFromAiList,
        )

        # Parse the response
        parsed_response = json.loads(response)
        patterns = parsed_response['patterns']

        # Get the current date and time
        current_time = datetime.now()
        
        # Process patterns
        processed_patterns = await self._process_patterns(patterns, current_time)
        
        return processed_patterns

    async def _process_patterns(self, patterns, current_time):
        for pattern in patterns:
            # Generate a UUID for the pattern
            pattern["uuid"] = str(uuid.uuid4())

            # Create and upload images
            folder_name = await self._create_and_upload_images(pattern, current_time)
            
            # Process Printify integration
            await self._handle_printify_integration(pattern, current_time, folder_name)

        return patterns

    async def _create_and_upload_images(self, pattern, current_time):
        folder_name = f"./img/{current_time.strftime('%Y-%m-%d_%H-%M-%S')}"
        
        # Create the directory if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Generate image for each color
        for color in self.text_colors:
            hex_value = color.get("hex")
            create_text_image(
                text=pattern.get("tshirt_text"),
                height=2000,
                width=2000,
                file_name=f"{folder_name}/{pattern.get('uuid')}{hex_value}.png",
                color="#" + hex_value
            )

        # Upload to GitHub
        directory_with_images = f"{folder_name}/"
        github_repository_url = os.getenv("GH_UPLOAD_REPO")
        personal_access_token = os.getenv("GH_PAT")
        
        uploader = GithubUploader(
            directory_with_images,
            github_repository_url,
            personal_access_token
        )
        uploader.upload()

        return folder_name

    async def _handle_printify_integration(self, pattern, current_time, folder_name):
        url_prefix = os.getenv("GH_CONTENT_PREFIX")
        
        # Upload images to Printify
        for color in self.text_colors:
            hex_value = color.get("hex")
            image_url = f"{url_prefix}/{current_time.strftime('%Y-%m-%d_%H-%M-%S')}/{
                quote(pattern.get('uuid'))}{hex_value}.png"
            image_id = self.printify.upload_image(image_url)
            color["image_id"] = image_id

        # Create and publish product
        variants, _, _ = self.printify.get_all_variants(self.blueprint, self.printer)
        product = self.printify.create_product(
            blueprint_id=self.blueprint,
            print_provider_id=self.printer,
            variants=variants,
            title=pattern.get("product_name"),
            description=pattern.get("description"),
            marketing_tags=pattern.get("marketing_tags"),
            text_colors=self.text_colors
        )

        # Update pattern with product info
        pattern.update({
            "product_id": product,
            "image_ids": [color.get("image_id") for color in self.text_colors]
        })

        # Publish the product
        self.printify.publish_product(product)