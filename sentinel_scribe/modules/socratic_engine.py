"""
Module 8: Socratic Engine
Generates teaching content using Socratic method.
"""

from typing import Dict, Any
from config import SOCRATIC_PROMPT_TEMPLATE
from llm import get_llm


class SocraticEngine:
    """
    Generates educational content teaching security reasoning.
    """
    
    def generate_teaching(
        self,
        plan: Dict[str, Any],
        code: str,
        vulnerability_type: str = None
    ) -> Dict[str, str]:
        """
        Generate Socratic teaching content.
        
        Args:
            plan: Attack plan with vulnerability info
            code: Relevant code snippet
            vulnerability_type: Override vulnerability type
        
        Returns:
            Dict with questions, hint, and explanation
        """
        llm = get_llm()
        
        vuln_type = vulnerability_type or plan.get("vulnerability_type", "unknown")
        code_snippet = code[:500] if len(code) > 500 else code
        
        prompt = SOCRATIC_PROMPT_TEMPLATE.format(
            vulnerability_type=vuln_type,
            code_snippet=code_snippet
        )
        
        response = llm.generate(prompt, raw=True)
        
        # Parse response
        teaching = self._parse_teaching_response(response)
        
        return teaching
    
    def _parse_teaching_response(self, response: str) -> Dict[str, str]:
        """
        Parse teaching response into structured format.
        
        Args:
            response: LLM response
        
        Returns:
            Dict with questions, hint, explanation
        """
        lines = response.split('\n')
        
        result = {
            "questions": [],
            "hint": "",
            "explanation": ""
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if "QUESTIONS:" in line:
                current_section = "questions"
                continue
            elif "HINT:" in line:
                current_section = "hint"
                continue
            elif "EXPLANATION:" in line:
                current_section = "explanation"
                continue
            
            if line and current_section:
                if current_section == "questions":
                    if line.startswith("-"):
                        result["questions"].append(line[1:].strip())
                    elif line.startswith("?"):
                        result["questions"].append(line[1:].strip())
                    else:
                        result["questions"].append(line)
                elif current_section == "hint":
                    result["hint"] += line + " "
                elif current_section == "explanation":
                    result["explanation"] += line + " "
        
        result["hint"] = result["hint"].strip()
        result["explanation"] = result["explanation"].strip()
        
        return result
    
    def generate_learning_objectives(
        self,
        vulnerability_type: str
    ) -> Dict[str, str]:
        """
        Generate learning objectives for a vulnerability type.
        
        Args:
            vulnerability_type: Type of vulnerability (SQL injection, XSS, etc.)
        
        Returns:
            Dict with learning objectives
        """
        prompt = f"""As a security educator, define learning objectives for {vulnerability_type}.
        
List 3 key concepts students should understand about {vulnerability_type}.
Format as:
CONCEPT 1:
CONCEPT 2:
CONCEPT 3:
"""
        
        llm = get_llm()
        response = llm.generate(prompt, raw=True)
        
        concepts = response.split("CONCEPT")[1:]
        
        return {
            "vulnerability_type": vulnerability_type,
            "concepts": [c.strip() for c in concepts][:3]
        }
