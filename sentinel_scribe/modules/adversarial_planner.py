"""
Module 2: Adversarial Planner
Identifies vulnerabilities via LLM reasoning.
"""

from typing import Dict, Any
from config import PLANNER_PROMPT_TEMPLATE
from llm import get_llm


class AdversarialPlanner:
    """
    Uses LLM to reason about code and identify vulnerability.
    Core reasoning engine that drives the entire pipeline.
    """
    
    def plan_attack(self, context: str) -> Dict[str, Any]:
        """
        Analyze code context and generate attack plan.
        
        Args:
            context: Structured code context from ContextLoader
        
        Returns:
            Dict with attack plan:
            {
                "entry_point": str,
                "data_flow": List[str],
                "sink": str,
                "vulnerability_type": str,
                "exploit_strategy": str,
                "payload_hint": str,
                "confidence": float
            }
        """
        llm = get_llm()
        
        prompt = PLANNER_PROMPT_TEMPLATE + context
        
        response = llm.generate(prompt, raw=False)
        
        # Validate required fields
        required_fields = [
            "entry_point",
            "data_flow",
            "sink",
            "vulnerability_type",
            "exploit_strategy",
            "payload_hint"
        ]
        
        if isinstance(response, dict) and "error" not in response:
            # Add default confidence if missing
            if "confidence" not in response:
                response["confidence"] = 0.8
            return response
        else:
            # Return error structure
            return {
                "error": "Failed to generate plan",
                "llm_response": response,
                "entry_point": "unknown",
                "data_flow": [],
                "sink": "unknown",
                "vulnerability_type": "unknown",
                "exploit_strategy": "unknown",
                "payload_hint": "",
                "confidence": 0.0
            }
