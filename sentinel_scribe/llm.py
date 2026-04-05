"""
LLM Interface for Sentinel-Scribe
Handles communication with Ollama for local, offline reasoning.
"""

import requests
import json
from typing import Dict, Any
from config import OLLAMA_MODEL, OLLAMA_ENDPOINT
from utils import extract_json


class LLMInterface:
    """Interface to Ollama for offline LLM reasoning."""
    
    def __init__(self, model: str = OLLAMA_MODEL, endpoint: str = OLLAMA_ENDPOINT):
        self.model = model
        self.endpoint = endpoint
    
    def generate(self, prompt: str, raw: bool = False) -> str:
        """
        Generate response from LLM.
        
        Args:
            prompt: Input prompt
            raw: If True, return raw response. If False, extract JSON.
        
        Returns:
            Generated text or JSON dict
        """
        try:
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "error": f"Ollama returned status {response.status_code}",
                    "details": response.text
                }
            
            data = response.json()
            text = data.get("response", "")
            
            if raw:
                return text
            else:
                return extract_json(text)
        
        except requests.exceptions.ConnectionError:
            return {
                "error": "Cannot connect to Ollama",
                "hint": "Start Ollama: ollama serve"
            }
        except Exception as e:
            return {
                "error": f"LLM error: {str(e)}"
            }
    
    def is_available(self) -> bool:
        """Check if Ollama is reachable."""
        try:
            response = requests.get(
                f"{self.endpoint}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Global LLM instance
_llm = None


def get_llm() -> LLMInterface:
    """Get or create global LLM instance."""
    global _llm
    if _llm is None:
        _llm = LLMInterface()
    return _llm
