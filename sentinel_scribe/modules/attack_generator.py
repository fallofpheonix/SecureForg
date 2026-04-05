"""
Module 3: Attack Generator
Converts exploit strategy into executable payloads.
"""

from typing import List
import urllib.parse


class AttackGenerator:
    """
    Generates test payloads based on exploit strategy.
    """
    
    def generate_payloads(self, plan: dict) -> List[str]:
        """
        Create multiple payload variations for testing.
        
        Args:
            plan: Attack plan from AdversarialPlanner
        
        Returns:
            List of payload strings to test
        """
        base_payload = plan.get("payload_hint", "")
        
        if not base_payload:
            return []
        
        payloads = []
        
        # Original payload
        payloads.append(base_payload)
        
        # URL encoded
        payloads.append(urllib.parse.quote(base_payload))
        
        # Double encoded
        payloads.append(urllib.parse.quote(urllib.parse.quote(base_payload)))
        
        # With unicode escapes
        payloads.append(
            base_payload.encode('unicode-escape').decode('ascii')
        )
        
        return payloads
    
    def generate_custom_payloads(
        self,
        base: str,
        variations: List[str]
    ) -> List[str]:
        """
        Generate custom payload variations.
        
        Args:
            base: Base payload
            variations: List of transformation names
                        ['url_encoded', 'double_encoded', 'unicode_escaped']
        
        Returns:
            List of payload variations
        """
        payloads = [base]
        
        if 'url_encoded' in variations:
            payloads.append(urllib.parse.quote(base))
        
        if 'double_encoded' in variations:
            payloads.append(urllib.parse.quote(urllib.parse.quote(base)))
        
        if 'unicode_escaped' in variations:
            payloads.append(base.encode('unicode-escape').decode('ascii'))
        
        return payloads
