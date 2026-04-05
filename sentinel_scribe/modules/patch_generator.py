"""
Module 6: Patch Generator
Generates security fixes via LLM.
"""

from typing import Dict, Any
from config import PATCH_PROMPT_TEMPLATE
from llm import get_llm


class PatchGenerator:
    """
    Uses LLM to generate secure code fixes.
    """
    
    def generate_patch(
        self,
        code: str,
        plan: Dict[str, Any]
    ) -> str:
        """
        Generate security patch for vulnerability.
        
        Args:
            code: Original vulnerable code
            plan: Attack plan with vulnerability info
        
        Returns:
            Unified diff of the fix
        """
        llm = get_llm()
        
        vulnerability_type = plan.get("vulnerability_type", "unknown")
        exploit_strategy = plan.get("exploit_strategy", "")
        
        prompt = PATCH_PROMPT_TEMPLATE.format(
            vulnerability_type=vulnerability_type,
            exploit_strategy=exploit_strategy
        )
        
        prompt += f"\n\n{code}"
        
        response = llm.generate(prompt, raw=True)
        
        return response
    
    def apply_patch(
        self,
        original_code: str,
        patch: str
    ) -> str:
        """
        Apply unified diff patch to code.
        
        Args:
            original_code: Original code
            patch: Unified diff format patch
        
        Returns:
            Patched code
        """
        import difflib
        
        try:
            # Try to parse unified diff
            patch_lines = patch.split('\n')
            
            # Simple implementation - extract fixed code from diff
            fixed_lines = []
            in_fixed = False
            
            for line in patch_lines:
                if line.startswith('+++ fixed'):
                    in_fixed = True
                    continue
                elif line.startswith('---') or line.startswith('+++'):
                    continue
                elif in_fixed:
                    if line.startswith('+'):
                        fixed_lines.append(line[1:])
                    elif not line.startswith('-'):
                        fixed_lines.append(line)
            
            if fixed_lines:
                return '\n'.join(fixed_lines)
            
            # Fallback: return original if parsing fails
            return original_code
        
        except:
            return original_code
    
    def validate_patch_syntax(self, code: str) -> bool:
        """
        Check if patched code has valid syntax.
        
        Args:
            code: Code to validate
        
        Returns:
            True if syntax is valid
        """
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
