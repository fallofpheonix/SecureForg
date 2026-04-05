"""
Module 7: Validation Engine
Verifies fixes by re-running attacks against patched code.
"""

from typing import Tuple, List
from .sandbox_executor import SandboxExecutor
from .exploit_detector import ExploitDetector


class ValidationEngine:
    """
    Re-executes attacks against patched code to verify security improvement.
    """
    
    def __init__(self):
        self.executor = SandboxExecutor()
        self.detector = ExploitDetector()
    
    def validate_patch(
        self,
        original_code: str,
        patched_code: str,
        payloads: List[str]
    ) -> dict:
        """
        Test if patch blocks all attacks.
        
        Args:
            original_code: Original vulnerable code
            patched_code: Patched code
            payloads: List of attack payloads
        
        Returns:
            Validation report
        """
        original_results = []
        patched_results = []
        
        for payload in payloads:
            # Test original
            stdout, stderr, _ = self.executor.execute(original_code, payload)
            is_exploit = self.detector.detect_exploit(stdout, stderr)
            original_results.append(is_exploit)
            
            # Test patched
            stdout, stderr, _ = self.executor.execute(patched_code, payload)
            is_exploit = self.detector.detect_exploit(stdout, stderr)
            patched_results.append(is_exploit)
        
        report = {
            "payloads_tested": len(payloads),
            "original_vulnerabilities": sum(original_results),
            "patched_vulnerabilities": sum(patched_results),
            "payload_results": [
                {
                    "payload_index": i,
                    "original_vulnerable": original_results[i],
                    "patched_vulnerable": patched_results[i],
                    "blocked": original_results[i] and not patched_results[i]
                }
                for i in range(len(payloads))
            ],
            "security_improved": any(original_results) and not any(patched_results),
            "all_blocked": not any(patched_results),
            "improvement_score": self._calculate_improvement(
                original_results,
                patched_results
            )
        }
        
        return report
    
    def _calculate_improvement(
        self,
        original_results: List[bool],
        patched_results: List[bool]
    ) -> float:
        """
        Calculate security improvement percentage.
        
        Returns:
            Score from 0.0 to 1.0
        """
        if not original_results:
            return 1.0
        
        original_vulns = sum(original_results)
        blocked = sum(1 for i in range(len(original_results))
                     if original_results[i] and not patched_results[i])
        
        if original_vulns == 0:
            return 1.0
        
        return blocked / original_vulns
    
    def run_regression_tests(
        self,
        code: str,
        test_cases: List[Tuple[str, str]]
    ) -> dict:
        """
        Run regression tests to ensure fix doesn't break functionality.
        
        Args:
            code: Code to test
            test_cases: List of (input, expected_output) tuples
        
        Returns:
            Regression test report
        """
        passed = 0
        failed = 0
        results = []
        
        for test_input, expected in test_cases:
            stdout, stderr, _ = self.executor.execute(code, test_input)
            
            match = expected in stdout or expected == stdout.strip()
            if match:
                passed += 1
            else:
                failed += 1
            
            results.append({
                "input": test_input,
                "expected": expected,
                "got": stdout.strip(),
                "passed": match
            })
        
        return {
            "total_tests": passed + failed,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / (passed + failed) if (passed + failed) > 0 else 0,
            "results": results
        }
