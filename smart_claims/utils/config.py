import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """
    Centralized configuration management for the Refund Processing System
    """
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'AI Refund Processing System')
    
    # Model Configurations
    SENTIMENT_MODEL = os.getenv(
        'SENTIMENT_MODEL', 
        'ProsusAI/finbert'
    )
    IMAGE_CLASSIFICATION_MODEL = os.getenv(
        'IMAGE_CLASSIFICATION_MODEL', 
        'gpt-4o-mini-2024-07-18'
    )
    REFUND_ESTIMATION_MODEL = os.getenv(
        'REFUND_ESTIMATION_MODEL', 
        'gpt-4o'
    )