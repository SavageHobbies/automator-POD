import os
from typing import List, Dict
import openai
from dotenv import load_dotenv

class DesignGenerator:
    """Service for generating design ideas and content using AI."""

    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

    async def generate_design_concept(self, prompt: str) -> Dict[str, str]:
        """Generate a design concept including title, description, and text content.

        Args:
            prompt: User's design idea or prompt

        Returns:
            Dict containing title, description, and design text
        """
        system_prompt = """You are a creative t-shirt designer. Generate a unique design concept 
        based on the given prompt. Include a product title, marketing description, and the actual 
        text/content that should appear on the t-shirt. Keep the design text concise and impactful."""

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            # Parse the response to extract title, description, and design text
            content = response.choices[0].message.content

            # Simple parsing - you might want to make this more robust
            lines = content.split("\n")
            title = next(line for line in lines if line.strip()).strip()
            description = "\n".join(lines[1:]).strip()

            return {
                "title": title,
                "description": description,
                "design_text": title  # For simplicity, using title as design text
            }

        except Exception as e:
            raise Exception(f"Failed to generate design concept: {str(e)}")

    async def generate_design_variations(self, concept: Dict[str, str], count: int = 3) -> List[Dict[str, str]]:
        """Generate variations of a design concept.

        Args:
            concept: Original design concept
            count: Number of variations to generate

        Returns:
            List of design variations
        """
        system_prompt = f"""Based on the original design concept:
        Title: {concept['title']}
        Description: {concept['description']}

        Generate {count} unique variations of this design. Each variation should have a similar theme 
        but be distinct. Keep the text concise and impactful."""

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate {count} variations"}
                ],
                temperature=0.8
            )

            content = response.choices[0].message.content
            variations = []

            # Parse variations - this is a simple implementation
            parts = content.split("\n\n")
            for part in parts[:count]:
                if part.strip():
                    variations.append({
                        "title": part.strip().split("\n")[0],
                        "description": "\n".join(part.strip().split("\n")[1:]),
                        "design_text": part.strip().split("\n")[0]
                    })

            return variations

        except Exception as e:
            raise Exception(f"Failed to generate design variations: {str(e)}")

    async def generate_tags(self, design: Dict[str, str], count: int = 5) -> List[str]:
        """Generate relevant tags for the design.

        Args:
            design: Design data including title and description
            count: Number of tags to generate

        Returns:
            List of relevant tags
        """
        system_prompt = f"""Based on this t-shirt design:
        Title: {design['title']}
        Description: {design['description']}

        Generate {count} relevant tags for marketing and SEO. Tags should be single words or short 
        phrases that people might search for."""

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate {count} tags"}
                ],
                temperature=0.6
            )

            content = response.choices[0].message.content
            tags = [tag.strip() for tag in content.split("\n") if tag.strip()]
            return tags[:count]

        except Exception as e:
            raise Exception(f"Failed to generate tags: {str(e)}")