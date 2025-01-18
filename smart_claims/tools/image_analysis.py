import base64
import logging
from PIL import Image
from typing import List, Dict, Any
from openai import OpenAI
from smart_claims.utils.config import Config
from smart_claims.utils.prompts import IMAGE_ANALYSIS_SYSTEM_PROMPT
from smart_claims.utils.data_models import ImageAnalysisResponse

# Supports one opensource model and GPT-4o
if Config.IMAGE_ANALYSIS_MODEL not in ['gpt-4o-mini', 'gpt-4o']:
    from transformers import AutoModelForCausalLM, AutoProcessor
    from transformers import BitsAndBytesConfig
    import torch
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype="float16",
        bnb_4bit_use_double_quant=True
    )

    # Note: set _attn_implementation='eager' if you don't have flash_attn installed
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3.5-vision-instruct" ,
        device_map="cuda",
        trust_remote_code=True,
        torch_dtype="auto",
        _attn_implementation='eager',
        quantization_config=quantization_config
    )

    # for best performance, use num_crops=4 for multi-frame, num_crops=16 for single-frame.
    processor = AutoProcessor.from_pretrained(
        "microsoft/Phi-3.5-vision-instruct",
        trust_remote_code=True,
        num_crops=4
    )
else:
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
        if Config.IMAGE_ANALYSIS_MODEL in ['gpt-4o-mini', 'gpt-4o']:
            try:
                # Encode image
                content = [
                    {
                        "type": "text", 
                        "text": f"""
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
                    model=Config.IMAGE_ANALYSIS_MODEL,
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
        else:
            try:
                images = []
                placeholder = f"""
                Product Information:
                    - Product Name: {product_info['product_name']}
                    - Product Description: {product_info['product_description']}
                    
                Now, carefully examine these product images.
                """
                
                for image_path in image_paths:
                    images.append(Image.open(image_path))
                    placeholder += f"<|image_{len(images)}|>\n"
                
                placeholder += "Return the detected detects followed by an overall defect score separated by \n-----\n"
                messages = [
                    {
                        "role": "user",
                        "content": IMAGE_ANALYSIS_SYSTEM_PROMPT + placeholder
                    }
                ]
                
                prompt = processor.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )

                inputs = processor(prompt, images, return_tensors="pt").to(device)

                generate_ids = model.generate(
                    **inputs,
                    eos_token_id= processor.tokenizer.eos_token_id,
                    max_new_tokens=256,
                    temperature=0.0,
                )

                generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
                response = processor.batch_decode(
                    generate_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False
                )[0].split("-----")
                
                return {
                    'image_path': image_paths,
                    'error': None,
                    'detected_defects': response[0],
                    'defect_score': response[1],
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
    product_info = {
        "product_name": "Panda Stuffed Animal",
        "product_description": "A cute stuffed animal in the shape of a Panda",
    }
    product_image_paths = ["test/data/images/image1.jpg", "test/data/images/image2.jpg", "test/data/images/image3.jpg"]
    
    results = image_tool.analyze_images(product_image_paths)
    for result in results:
        print(result)