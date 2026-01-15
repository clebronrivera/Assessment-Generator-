"""
AI Client Interface
Simple wrapper that works with OpenAI, Anthropic, or any AI API
"""

from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class AIClient(ABC):
    """Base class for AI clients."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt."""
        pass
    
    def complete(self, prompt: str, **kwargs) -> str:
        """Alias for generate() for backward compatibility."""
        return self.generate(prompt, **kwargs)


class OpenAIClient(AIClient):
    """
    OpenAI API client.
    Requires: pip install openai
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4)
        """
        try:
            import openai
            self.openai = openai
            self.api_key = api_key
            self.model = model
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: The prompt to send
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated text
        """
        response = self.client.chat.completions.create(
            model=kwargs.get('model', self.model),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=kwargs.get('temperature', 0.7),
            max_tokens=kwargs.get('max_tokens', 2000)
        )
        
        return response.choices[0].message.content


class AnthropicClient(AIClient):
    """
    Anthropic Claude API client.
    Requires: pip install anthropic
    """
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Anthropic client.
        
        Args:
            api_key: Anthropic API key
            model: Model to use (default: claude-sonnet-4)
        """
        try:
            import anthropic
            self.anthropic = anthropic
            self.api_key = api_key
            self.model = model
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Anthropic API.
        
        Args:
            prompt: The prompt to send
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            Generated text
        """
        response = self.client.messages.create(
            model=kwargs.get('model', self.model),
            max_tokens=kwargs.get('max_tokens', 2000),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=kwargs.get('temperature', 0.7)
        )
        
        return response.content[0].text


class MockAIClient(AIClient):
    """
    Mock AI client for testing without API calls.
    Returns a sample passage for testing.
    """
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Return mock passage for testing.
        
        Args:
            prompt: The prompt (not used, but required by interface)
            **kwargs: Additional parameters (not used)
            
        Returns:
            Mock passage text
        """
        # Extract grade from prompt if possible
        grade = "2"  # default
        if "Grade 2" in prompt or "grade: 2" in prompt:
            grade = "2"
        
        # Return grade-appropriate mock passage
        if grade == "1":
            return """Jake saw a big red ball. He wanted to play with it. Jake ran to get the ball. His dog Max ran with him. They played catch in the yard. Jake threw the ball high. Max jumped and caught it. They had fun together. Then Mom called them in for lunch. Jake and Max were tired. They sat down to rest."""
        
        elif grade == "2":
            return """Sam and Mia walked to the park after school. The sky was bright, and a cool wind moved the leaves. At the gate, they saw a small brown dog with a red collar. The dog looked nervous and kept sniffing the ground.

Mia knelt down and read the tag. "This dog is named Pepper," she said. Sam held out his hand. Pepper stepped closer and licked his fingers. They looked around, but no one called for Pepper. Mia said, "We should help."

They led Pepper to the community center office. The helper there called the number on the tag. While they waited, Sam gave Pepper some water, and Mia sat near him so he felt safe. Soon, a woman ran in and hugged Pepper. She thanked Sam and Mia for staying calm and doing the right thing."""
        
        else:
            return """Maya noticed something strange in her backyard. The old oak tree had a small door carved into its trunk. She had lived here for ten years and never seen it before. The door was only six inches tall, made of smooth dark wood with tiny brass hinges. Maya bent down to look closer. Through the keyhole, she could see a soft golden light.

Her little brother called from the house, but Maya couldn't look away. She touched the door gently with one finger. It swung open, and warm air rushed out, carrying the smell of cinnamon and pine. Inside, a spiral staircase led down into the tree. Maya knew she should tell someone, but curiosity pulled at her.

She took a deep breath and made her choice. Tomorrow she would explore. Tonight, she closed the little door carefully and marked the spot with a small white stone. Some mysteries, she thought, needed time and planning."""


# Helper function to create client from API key
def create_ai_client(api_key: str, provider: str = "anthropic") -> AIClient:
    """
    Create an AI client based on provider.
    
    Args:
        api_key: API key for the provider
        provider: "openai", "anthropic", or "mock"
        
    Returns:
        AIClient instance
    """
    provider = provider.lower()
    
    if provider == "openai":
        return OpenAIClient(api_key)
    elif provider == "anthropic":
        return AnthropicClient(api_key)
    elif provider == "mock":
        return MockAIClient()
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'anthropic', or 'mock'")
