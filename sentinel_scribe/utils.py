"""
Utility functions for Sentinel-Scribe system.
"""

import json
import re
from typing import Any, Dict


def extract_json(text: str) -> Dict[str, Any]:
    """
    Extract and parse JSON from text response.
    Handles cases where JSON is embedded in markdown or other text.
    """
    # Try direct JSON parse first
    text = text.strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON block (handles ```json...```)
    json_match = re.search(r'```(?:json)?\s*(\{[^`]*\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find any valid JSON object in text
    brace_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Fallback: return error structure
    return {
        "error": "Failed to parse JSON",
        "raw_text": text[:200]
    }


def format_code_block(code: str, language: str = "python") -> str:
    """Format code as markdown block."""
    return f"```{language}\n{code}\n```"


def format_diff(original: str, fixed: str) -> str:
    """
    Create a simplified unified diff between original and fixed code.
    """
    import difflib
    
    original_lines = original.splitlines(keepends=True)
    fixed_lines = fixed.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        fixed_lines,
        fromfile='original',
        tofile='fixed',
        lineterm=''
    )
    
    return ''.join(diff)


def safe_filename(text: str) -> str:
    """Convert text to safe filename."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)
