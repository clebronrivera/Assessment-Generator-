"""
Template Loader Utility
Loads and renders Jinja2 templates for assessment generation.
"""

from pathlib import Path
from jinja2 import Template
from typing import Dict, Any


class TemplateLoader:
    """Loads and renders Jinja2 templates."""
    
    def __init__(self, template_dir: str = None):
        """
        Initialize template loader.
        
        Args:
            template_dir: Path to templates directory (default: templates/prompts)
        """
        if template_dir is None:
            # Default to templates/prompts relative to project root
            template_dir = "templates/prompts"
        
        self.template_dir = Path(template_dir)
        
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {self.template_dir}")
    
    def load(self, template_name: str) -> Template:
        """
        Load a Jinja2 template.
        
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
    
    def render(self, template_name: str, **variables) -> str:
        """
        Load and render a template with variables.
        
        Args:
            template_name: Name of template file
            **variables: Variables to pass to template
            
        Returns:
            Rendered template as string
        """
        template = self.load(template_name)
        return template.render(**variables)
