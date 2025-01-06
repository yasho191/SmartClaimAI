import base64
import logging
from typing import List, Dict, Any
from openai import OpenAI
from smart_claims.utils.config import Config
from smart_claims.utils.prompts import IMAGE_ANALYSIS_SYSTEM_PROMPT
from smart_claims.utils.data_models import ImageAnalysisResponse

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class ImageAnalysisTool:
    """
    Image analysis tool using GPT-4o for advanced visual inspection
    """

    def encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 for OpenAI API
        
        :param image_path: Path to the image file
        :return: Base64 encoded image string
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logging.error(f"Image encoding failed: {e}")

    def analyze_images(self, image_paths: List[str], product_info: Dict) -> Dict[str, Any]:
        """
        Analyze an image using GPT-4o-mini vision capabilities
        
        :param image_path: Path to the image file
        :return: Dictionary with image analysis results
        """
        try:
            # Encode image
            content = [
                {
                    "type": "text", 
                    "text": """
                    Product Information:
                    - Product Name: {product_info['product_name']}
                    - Product Description: {product_info['product_description']}
                    
                    Now, carefully examine these product images. 
                    """
                },
                            
            ]
            
            for image_path in image_paths:
                base64_image = self.encode_image(image_path)
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                        "detail": "low"
                    }
                )
            
            # Prepare GPT-4o vision request
            response = client.chat.completions.create(
                model=Config.IMAGE_CLASSIFICATION_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": IMAGE_ANALYSIS_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=300,
                temperature=0,
                response_format=ImageAnalysisResponse
            )
            
            # Extract analysis from response
            image_analysis = response.choices[0].message.parsed
            
            return {
                'image_path': image_paths,
                'error': None,
                'detected_defects': image_analysis.detected_defects,
                'defect_score': image_analysis.defect_score,
            }
        
        except Exception as e:
            logging.error(f"Image analysis failed for {image_paths}: {e}")
            return {
                'image_paths': image_paths,
                'error': str(e),
                'detected_defects': None,
                'defect_score': None,
            }



if __name__ == "__main__":
    # Example usage
    image_tool = ImageAnalysisTool()
    
    product_image_paths = ["test/data/images/image1.jpg", "test/data/images/image2.jpg", "test/data/images/image3.jpg"]
    
    results = image_tool.analyze_images(product_image_paths)
    for result in results:
        print(result)