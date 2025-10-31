"""
Response Generation Module for Hindi AI Assistant
Combines rule-based responses with optional LLM integration
"""

import re
from typing import Dict, List, Optional
import os

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class ResponseGenerator:
    """
    Generate intelligent Hindi responses using rules and optional LLM
    """
    
    def __init__(self, use_llm: bool = False):
        """
        Initialize the response generator
        
        Args:
            use_llm: Whether to use OpenAI for complex queries (requires API key)
        """
        self.use_llm = use_llm and OPENAI_AVAILABLE
        if self.use_llm and not OPENAI_AVAILABLE:
            print("Warning: OpenAI not available, falling back to rule-based responses")
        
        # Define response patterns and rules
        self.response_rules = {
            'greeting': {
                'patterns': ['नमस्ते', 'नमस्कार', 'हैलो', 'स्वागत', 'प्रणाम', 'अरे'],
                'responses': [
                    'नमस्ते! मैं आपकी क्या मदद कर सकता हूं?',
                    'नमस्कार! मैं ठीक हूं, बताइए आप कैसे हैं?',
                    'हैलो! आपका स्वागत है। मैं यहां आपकी मदद के लिए हूं।'
                ]
            },
            'name_question': {
                'patterns': ['नाम', 'कौन हो', 'क्या नाम'],
                'responses': [
                    'मेरा नाम हिंदी AI सहायक है। आप मुझे कुछ भी पूछ सकते हैं।',
                    'मैं एक हिंदी भाषा AI सहायक हूं। आपका नाम क्या है?'
                ]
            },
            'weather': {
                'patterns': ['मौसम', 'तापमान', 'गर्मी', 'ठंड', 'बारिश'],
                'responses': [
                    'क्षमा करें, मेरे पास वास्तविक मौसम की जानकारी नहीं है।',
                    'मैं मौसम के बारे में जानकारी नहीं दे सकता, लेकिन मैं आपकी अन्य मदद कर सकता हूं।'
                ]
            },
            'time': {
                'patterns': ['समय', 'कितने बजे', 'क्या वक्त'],
                'responses': [
                    'क्षमा करें, मेरे पास वर्तमान समय की जानकारी नहीं है।'
                ]
            },
            'how_are_you': {
                'patterns': ['कैसे हो', 'कैसी है', 'ठीक हो', 'क्या हाल'],
                'responses': [
                    'मैं ठीक हूं, धन्यवाद! आप कैसे हैं?',
                    'मैं बिल्कुल ठीक हूं। आपका क्या हाल है?'
                ]
            },
            'what_can_you_do': {
                'patterns': ['क्या कर सकते', 'क्या कर सकती', 'क्या फायदा', 'कैसे मदद'],
                'responses': [
                    'मैं हिंदी में बात कर सकता हूं, प्रश्नों का उत्तर दे सकता हूं, और आपकी मदद कर सकता हूं।',
                    'मैं हिंदी में संवाद कर सकता हूं। आप मुझसे कोई भी सवाल पूछ सकते हैं।'
                ]
            },
            'thank_you': {
                'patterns': ['धन्यवाद', 'शुक्रिया', 'बहुत अच्छे', 'अच्छा'],
                'responses': [
                    'आपका स्वागत है! कोई भी मदद चाहिए तो बताइए।',
                    'खुशी हुई मदद करके। क्या और कुछ है?'
                ]
            },
            'farewell': {
                'patterns': ['अलविदा', 'नमस्ते', 'बाय', 'मिलते', 'चलते'],
                'responses': [
                    'अलविदा! जल्द ही मिलते हैं।',
                    'नमस्ते! बाद में मिलेंगे। खुश रहें!'
                ]
            },
            'unknown': {
                'patterns': ['.*'],  # Catch all
                'responses': [
                    'क्षमा करें, मैं यह समझ नहीं पाया। क्या आप फिर से प्रश्न पूछ सकते हैं?',
                    'मुझे इस बारे में जानकारी नहीं है। कोई अन्य प्रश्न है?',
                    'मैं इस प्रश्न का उत्तर नहीं जानता। कुछ और पूछिए।'
                ]
            }
        }
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate response based on user input
        
        Args:
            user_input: User's text input in Hindi
            
        Returns:
            Generated Hindi response
        """
        if not user_input or user_input.strip() == '':
            return 'क्षमा करें, मैं आपको सुन नहीं पाया।'
        
        user_input_lower = user_input.lower().strip()
        
        # Try rule-based matching first
        response = self._match_rule(user_input_lower)
        
        # If LLM enabled and no good rule match, use LLM
        if self.use_llm and response == self._get_default_response():
            llm_response = self._get_llm_response(user_input)
            if llm_response:
                return llm_response
        
        return response
    
    def _match_rule(self, user_input: str) -> str:
        """
        Match user input against predefined rules
        
        Args:
            user_input: Lowercase user input
            
        Returns:
            Matched response or default response
        """
        import random
        
        for category, data in self.response_rules.items():
            if category == 'unknown':
                continue
                
            for pattern in data['patterns']:
                if pattern.lower() in user_input:
                    return random.choice(data['responses'])
        
        # Return default response if no match
        return self._get_default_response()
    
    def _get_default_response(self) -> str:
        """Get default unknown response"""
        import random
        return random.choice(self.response_rules['unknown']['responses'])
    
    def _get_llm_response(self, user_input: str) -> Optional[str]:
        """
        Get response from OpenAI LLM
        
        Args:
            user_input: User's input
            
        Returns:
            LLM generated response or None
        """
        if not OPENAI_AVAILABLE:
            return None
            
        try:
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "आप एक मित्रतापूर्ण हिंदी भाषी AI सहायक हैं। संक्षिप्त और उपयोगी उत्तर दें। सदैव हिंदी में बात करें।"
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return None


def test_response_generator():
    """Test function for response generator"""
    generator = ResponseGenerator(use_llm=False)
    
    test_inputs = [
        "नमस्ते, आप कैसे हैं?",
        "मेरा नाम क्या है?",
        "आज मौसम कैसा है?",
        "आप क्या कर सकते हैं?"
    ]
    
    for input_text in test_inputs:
        response = generator.generate_response(input_text)
        print(f"\nInput: {input_text}")
        print(f"Response: {response}")


if __name__ == "__main__":
    test_response_generator()

