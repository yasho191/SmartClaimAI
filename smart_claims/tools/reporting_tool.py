from typing import Dict
from openai import OpenAI
from smart_claims.utils.config import Config
from smart_claims.utils.prompts import REFUND_ESTIMATION_PROMPT
from smart_claims.utils.data_models import RefundEstimationResponse

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class RefundEstimationTool:
    """
    Sentiment analysis tool using Hugging Face transformers
    """
    def generate_report(self, sentiment_analysis, image_analysis, claim_info) -> Dict:
        try:
            # Prepare GPT-4o vision request
            content = [
                {
                    "type": "text",
                    "text": f"""
                    Based on the sentiment analysis of the customer's review and the image analysis of the product images, 
                    please provide an estimate of the refund amount for the claim using the following details:
                    
                    - Product ID: {claim_info.product_id}
                    - Product Name: {claim_info.product_name}
                    - Product Cost: ${claim_info.product_cost}
                    
                    - Customer Review: {claim_info.product_review}
                    - Sentiment Score: {sentiment_analysis.sentiment_score}
                    - Sentiment: {sentiment_analysis.sentiment_label}
                    
                    - Defects Detected: {image_analysis.detected_defects}
                    - Defect Score: {image_analysis.defect_score}
                    """
                }
            ]
            response = client.chat.completions.create(
                model=Config.REFUND_ESTIMATION_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": REFUND_ESTIMATION_PROMPT
                    },
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                max_tokens=300,
                temperature=0,
                response_format=RefundEstimationResponse
            )

            # Extract analysis from response
            final_analysis = response.choices[0].message.parsed
            return {
                'refund_amount': final_analysis.refund_amount,
                'refund_status': final_analysis.refund_status,
                'refund_reason': final_analysis.refund_reason,
                'refund_notes': final_analysis.refund_notes,
                'error': None}
        
        except Exception as e:
            return {
                'refund_amount': None,
                'refund_status': None,
                'refund_reason': None,
                'refund_notes': None,
                'error': str(e)
            }


# Test
if __name__ == "__main__":
    # Example usage
    from utils.data_models import SentimentAnalysisResponse, ImageAnalysisResponse, RefundClaim
    
    sentiment_analysis = SentimentAnalysisResponse(
        sentiment_score=0.8,
        sentiment_label="Positive"
    )
    
    image_analysis = ImageAnalysisResponse(
        detected_defects="Scratch on screen, Dent on back",
        defect_score=0.6
    )
    
    claim_info = RefundClaim(
        product_id="12345",
        product_name="Smartphone",
        product_cost=500,
        product_review="The phone is great but has a scratch on the screen and a dent on the back."
    )
    
    refund_tool = RefundEstimationTool()
    refund_tool.generate_report(sentiment_analysis, image_analysis, claim_info)