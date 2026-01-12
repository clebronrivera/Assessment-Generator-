"""
Base Generator Class
All assessment generators inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from jinja2 import Template
from pathlib import Path
import json


class BaseGenerator(ABC):
    """
    Abstract base class for all assessment generators.
    Provides common functionality for template loading, rendering, and validation.
    """
    
    def __init__(self, banks_module, template_dir: str = "templates/prompts"):
        """
        Initialize the generator.
        
        Args:
            banks_module: The src.banks module with all bank functions
            template_dir: Path to template directory
        """
        self.banks = banks_module
        self.template_dir = Path(template_dir)
        
    def load_template(self, template_name: str) -> Template:
        """
        Load a Jinja2 template from the templates directory.
        
        Args:
            template_name: Name of template file (e.g., 'orf_passage.j2')
            
        Returns:
            Jinja2 Template object
        """
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        return Template(template_content)
    
    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Load and render a template with variables.
        
        Args:
            template_name: Name of template file
            variables: Dictionary of variables for template
            
        Returns:
            Rendered prompt as string
        """
        template = self.load_template(template_name)
        return template.render(**variables)
    
    @abstractmethod
    def generate(self, **kwargs) -> Dict[str, Any]:
        """
        Generate assessment content.
        Must be implemented by subclasses.
        
        Returns:
            Dictionary with generated content
        """
        pass
    
    @abstractmethod
    def validate(self, output: Dict[str, Any]) -> bool:
        """
        Validate generated output.
        Must be implemented by subclasses.
        
        Args:
            output: Generated content to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def call_ai(self, prompt: str, ai_client) -> str:
        """
        Call AI API with prompt.
        
        Args:
            prompt: The prompt to send
            ai_client: AI client object (OpenAI, Anthropic, etc.)
            
        Returns:
            AI response as string
        """
        # This will be implemented by the specific AI client
        # For now, it's a placeholder that generators can override
        if hasattr(ai_client, 'generate'):
            return ai_client.generate(prompt)
        else:
            raise NotImplementedError("AI client must have a 'generate' method")
    
    def save_output(self, output: Dict[str, Any], filepath: str) -> None:
        """
        Save generated output to file.
        
        Args:
            output: Generated content
            filepath: Where to save
        """
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
    
    def log_generation(self, output: Dict[str, Any]) -> None:
        """
        Log which banks were used for this generation.
        Helps with auditing and anti-drift tracking.
        
        Args:
            output: Generated content with metadata
        """
        if 'bank_usage' in output:
            print("\n[Bank Usage Report]")
            for bank, usage in output['bank_usage'].items():
                print(f"  {bank}: {usage}")
