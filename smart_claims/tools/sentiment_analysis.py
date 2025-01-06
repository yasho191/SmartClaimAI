import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import Dict, Any
from smart_claims.utils.config import Config

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = AutoTokenizer.from_pretrained(Config.SENTIMENT_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(Config.SENTIMENT_MODEL)
model.to(device)

class SentimentAnalysisTool:
    """
    Sentiment analysis tool using Hugging Face transformers
    """
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of given text
        
        :param text: Input text to analyze
        :return: Dictionary with sentiment analysis results
        """
        try:
            # Tokenize and prepare input
            inputs = tokenizer(text, return_tensors='pt', 
                                    truncation=True, 
                                    max_length=512).to(self.device)
            
            # Perform inference
            with torch.no_grad():
                outputs = model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
                
            # Get results
            sentiment_scores = probabilities.cpu().numpy()
            sentiment_class = sentiment_scores.argmax()
            label_mapping = model.config.id2label[sentiment_class]
            
            return {
                'text': text,
                'sentiment_label': label_mapping,
                'sentiment_score': sentiment_scores[sentiment_class],
                'error': None
            }
        except Exception as e:
            return {
                'text': text,
                'sentiment_label': None,
                'sentiment_score': None,
                'error': str(e)
            }


if __name__ == "__main__":
    # Example usage
    tool = SentimentAnalysisTool()
    result = tool.analyze_sentiment("I love the new design of your website!")
    print(result)