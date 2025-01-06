import openai
import uuid
from datetime import datetime, timedelta
from crewai.flow.flow import Flow, listen, start
from smart_claims.tools.sentiment_analysis import SentimentAnalysisTool
from smart_claims.tools.image_analysis import ImageAnalysisTool
from smart_claims.tools.reporting_tool import RefundEstimationTool
from smart_claims.utils.config import Config
from smart_claims.utils.data_models import RefundClaim, SentimentAnalysisResponse, ImageAnalysisResponse, RefundEstimationResponse


# Configure OpenAI
openai.api_key = Config.OPENAI_API_KEY

class ClaimRefundFlow(Flow):

    @start
    def initialize_claim_refund_flow(self, customer_claim: dict) -> RefundClaim:
        """
        Initialize the claim refund flow
        """
        claim_object = RefundClaim(**customer_claim)
        claim_object.claim_id = str(uuid.uuid4())
        
        # Check if claim date is less than 90 days from order date
        # If not, reject the claim
        claim_date = datetime.strptime(claim_object.claim_date, "%Y-%m-%d")
        order_date = datetime.strptime(claim_object.order_date, "%Y-%m-%d")
        if claim_date > order_date + timedelta(days=90):
            claim_object.refund_amount = 0.0
            claim_object.refund_status = "Rejected"
            claim_object.refund_reason = "Claim submitted after 90 days. The prduct is no longer in warranty."
        
        return claim_object
    
    @listen('initialize_claim_refund_flow')
    def analyse_sentiment_and_images(self, claim_object: RefundClaim) -> RefundClaim:
        """
        Analyze sentiment of product review and detect defects in product images
        """
        if claim_object.refund_status == "Rejected":
            return claim_object, None, None
        
        # Analyze sentiment of product review
        sentiment_tool = SentimentAnalysisTool()
        sentiment_results = sentiment_tool.run(claim_object.product_review)
        
        sentiment_analysis_response = SentimentAnalysisResponse(**sentiment_results)
        
        # Detect defects in product images
        image_tool = ImageAnalysisTool()
        image_results = image_tool.run(claim_object.product_images)
        image_analysis_response = ImageAnalysisResponse(**image_results)
        
        return claim_object, sentiment_analysis_response, image_analysis_response
    
    @listen('analyse_sentiment_and_images')
    def generate_claim_report(
            self, 
            claim_object: RefundClaim, 
            sentiment_response: SentimentAnalysisResponse | None, 
            image_response: ImageAnalysisResponse | None
        ) -> RefundClaim:
        """
        Generate a report based on sentiment analysis and image analysis results
        """
        refund_estimation = RefundEstimationTool()
        refund_response = refund_estimation.generate_report(sentiment_response, image_response, claim_object)
        
        if refund_response['error'] is None:
            claim_object.refund_amount = refund_response['refund_amount']
            claim_object.refund_status = refund_response['refund_status']
            claim_object.refund_reason = refund_response['refund_reason']
            claim_object.refund_notes = refund_response['refund_notes']
        else:
            claim_object.refund_amount = 0.0
            claim_object.refund_status = "Not Successfully Processed"
            claim_object.refund_reason = "Error processing refund request. Please try again later."
            
        return claim_object