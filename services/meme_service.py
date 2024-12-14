import logging
import os
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from content.types import MemeTemplate

logger = logging.getLogger(__name__)

class MemeService:
    def __init__(self):
        self.templates_dir = "assets/meme_templates"
        self.output_dir = "assets/generated_memes"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_meme(self, template: MemeTemplate, text: str) -> Optional[str]:
        """Generate a meme image and return its path"""
        try:
            template_path = os.path.join(self.templates_dir, template.filename)
            if not os.path.exists(template_path):
                logger.error(f"Template not found: {template_path}")
                return None

            # Generate unique filename for output
            output_filename = f"meme_{hash(text)}_{template.name}.png"
            output_path = os.path.join(self.output_dir, output_filename)

            # Create meme image
            with Image.open(template_path) as img:
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("assets/fonts/Impact.ttf", size=40)
                
                # Add text to image based on template configuration
                self._add_text_to_image(draw, text, template.text_positions, font)
                
                # Save the generated meme
                img.save(output_path, "PNG")
                logger.info(f"Generated meme saved to: {output_path}")
                return output_path

        except Exception as e:
            logger.error(f"Failed to generate meme: {e}")
            return None
    
    def _add_text_to_image(self, draw, text: str, positions: list, font):
        """Add text to the image at specified positions"""
        for position in positions:
            # Add text outline for better visibility
            x, y = position
            outline_color = "black"
            text_color = "white"
            outline_width = 2
            
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
            
            draw.text((x, y), text, font=font, fill=text_color)