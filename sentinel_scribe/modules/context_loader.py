"""
Module 1: Context Loader
Prepares structured input for LLM reasoning.
"""

from typing import Dict


class ContextLoader:
    """
    Loads and structures multi-file code context for LLM analysis.
    """
    
    def __init__(self):
        self.context = ""
        self.file_count = 0
    
    def load_files(self, files: Dict[str, str]) -> str:
        """
        Convert multiple files into structured context.
        
        Args:
            files: Dict mapping filenames to code content
        
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for filename, code in files.items():
            context_parts.append(f"<file path='{filename}'>\n{code}\n</file>")
            self.file_count += 1
        
        self.context = "\n\n".join(context_parts)
        return self.context
    
    def get_context(self) -> str:
        """Get loaded context."""
        return self.context
    
    def add_instruction(self, instruction: str) -> str:
        """Append instruction to context."""
        self.context += f"\n\n<instruction>\n{instruction}\n</instruction>"
        return self.context
    
    def reset(self):
        """Clear context."""
        self.context = ""
        self.file_count = 0
