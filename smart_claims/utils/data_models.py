from pydantic import BaseModel
from typing import List, Optional

class RefundClaim(BaseModel):
    """
    Represents a refund claim submitted by a customer
    """
    claim_id: str
    claim_date: str
    customer_id: str
    customer_name: str
    product_id: str
    product_name: str
    product_description: str
    product_cost: float
    order_id: str
    order_date: str
    product_review: str
    product_images: Optional[List[str]] = None
    refund_amount: float = 0.0
    refund_status: str = "Pending"
    refund_reason: str = "Under review"
    refund_notes: Optional[str] = None
    

class SentimentAnalysisResponse(BaseModel):
    """
    Represents a response to a sentiment analysis task
    """
    sentiment_score: float
    sentiment_label: str
    sentiment_details: str


class ImageAnalysisResponse(BaseModel):
    """
    Represents a response to an image analysis task
    """
    detected_defects: List[str]
    defect_score: float


class RefundEstimationResponse(BaseModel):
    """
    Represents a response to a report creation task
    """
    refund_amount: str
    refund_status: str
    refund_reason: str
    refund_notes: Optional[str] = None