"""
Pipeline Orchestrator
Main execution flow: PLAN → ATTACK → EXECUTE → VERIFY → FIX → RE-VERIFY → TEACH
"""

from typing import Dict, Any, Tuple
from modules import (
    ContextLoader,
    AdversarialPlanner,
    AttackGenerator,
    SandboxExecutor,
    ExploitDetector,
    PatchGenerator,
    ValidationEngine,
    SocraticEngine
)


class SentinelScribePipeline:
    """
    Main orchestrator implementing the 9-layer security analysis pipeline.
    """
    
    def __init__(self):
        self.context_loader = ContextLoader()
        self.planner = AdversarialPlanner()
        self.attack_gen = AttackGenerator()
        self.executor = SandboxExecutor()
        self.detector = ExploitDetector()
        self.patch_gen = PatchGenerator()
        self.validator = ValidationEngine()
        self.socratic = SocraticEngine()
        
        self.report = {}
    
    def run_full_pipeline(
        self,
        files: Dict[str, str],
        instruction: str = None
    ) -> Dict[str, Any]:
        """
        Execute complete pipeline: PLAN → ATTACK → EXECUTE → VERIFY → FIX → RE-VERIFY → TEACH
        
        Args:
            files: Dict of {filename: code}
            instruction: Optional analysis instruction
        
        Returns:
            Comprehensive analysis report
        """
        
        self.report = {
            "status": "running",
            "stages": {}
        }
        
        # STAGE 1: LOAD CONTEXT
        print("[1/9] Loading context...")
        context = self.context_loader.load_files(files)
        if instruction:
            context = self.context_loader.add_instruction(instruction)
        
        self.report["stages"]["context_load"] = {
            "files_loaded": self.context_loader.file_count,
            "context_size": len(context)
        }
        
        # STAGE 2: PLAN
        print("[2/9] Analyzing vulnerabilities...")
        plan = self.planner.plan_attack(context)
        
        if "error" in plan:
            self.report["status"] = "error"
            self.report["stages"]["planning"] = plan
            return self.report
        
        self.report["stages"]["planning"] = {
            "vulnerability_type": plan.get("vulnerability_type"),
            "entry_point": plan.get("entry_point"),
            "confidence": plan.get("confidence", 0),
            "exploit_strategy": plan.get("exploit_strategy")
        }
        
        # STAGE 3: GENERATE ATTACKS
        print("[3/9] Generating attack payloads...")
        payloads = self.attack_gen.generate_payloads(plan)
        
        self.report["stages"]["attack_generation"] = {
            "payload_count": len(payloads),
            "payloads": payloads[:3]  # Show first 3
        }
        
        # STAGE 4: EXECUTE ATTACKS
        print("[4/9] Executing attacks on original code...")
        original_code = files.get(list(files.keys())[0], "")
        
        original_results = []
        for i, payload in enumerate(payloads):
            stdout, stderr, _ = self.executor.execute(original_code, payload)
            is_exploit = self.detector.detect_exploit(stdout, stderr)
            original_results.append(is_exploit)
            print(f"  Payload {i+1}: {'VULNERABLE' if is_exploit else 'safe'}")
        
        self.report["stages"]["attack_execution"] = {
            "payloads_tested": len(payloads),
            "exploits_found": sum(original_results),
            "vulnerable": any(original_results)
        }
        
        # STAGE 5: GENERATE PATCH
        print("[5/9] Generating security patch...")
        patch = self.patch_gen.generate_patch(original_code, plan)
        
        self.report["stages"]["patch_generation"] = {
            "patch_generated": bool(patch),
            "patch_preview": patch[:200] if patch else ""
        }
        
        # STAGE 6: APPLY PATCH
        print("[6/9] Applying patch...")
        patched_code = self.patch_gen.apply_patch(original_code, patch)
        syntax_valid = self.patch_gen.validate_patch_syntax(patched_code)
        
        self.report["stages"]["patch_application"] = {
            "syntax_valid": syntax_valid,
            "code_changed": patched_code != original_code
        }
        
        # STAGE 7: RE-EXECUTE (VALIDATION)
        print("[7/9] Re-executing attacks on patched code...")
        validation = self.validator.validate_patch(
            original_code,
            patched_code,
            payloads
        )
        
        self.report["stages"]["validation"] = validation
        
        # STAGE 8: GENERATE TEACHING
        print("[8/9] Generating learning content...")
        teaching = self.socratic.generate_teaching(plan, original_code)
        
        self.report["stages"]["teaching"] = teaching
        
        # STAGE 9: METRICS & OUTPUT
        print("[9/9] Compiling metrics...")
        self.report["metrics"] = self._calculate_metrics(
            plan,
            original_results,
            validation,
            patched_code != original_code
        )
        
        self.report["status"] = "complete"
        
        return self.report
    
    def _calculate_metrics(
        self,
        plan: dict,
        original_results: list,
        validation: dict,
        patch_applied: bool
    ) -> dict:
        """Calculate final security metrics."""
        
        total_tests = len(original_results)
        original_vulns = sum(original_results)
        patched_vulns = validation.get("patched_vulnerabilities", 0)
        
        return {
            "vulnerability_type": plan.get("vulnerability_type", "unknown"),
            "attack_success_before": original_vulns,
            "attack_trials": total_tests,
            "attack_success_rate_before": original_vulns / total_tests if total_tests > 0 else 0,
            "attack_success_after": patched_vulns,
            "attack_success_rate_after": patched_vulns / total_tests if total_tests > 0 else 0,
            "security_improvement": validation.get("improvement_score", 0),
            "patch_applied": patch_applied,
            "exploit_blocked": not any([v.get("patched_vulnerable") for v in validation.get("payload_results", [])])
        }
    
    def print_report(self):
        """Pretty-print the analysis report."""
        
        if not self.report:
            print("No report generated yet.")
            return
        
        print("\n" + "="*70)
        print("SENTINEL-SCRIBE: ADVERSARIAL REASONING ENGINE - ANALYSIS REPORT")
        print("="*70 + "\n")
        
        # Status
        status = self.report.get("status", "unknown").upper()
        print(f"Status: {status}\n")
        
        # Planning Stage
        planning = self.report.get("stages", {}).get("planning", {})
        if planning and "error" not in planning:
            print("VULNERABILITY IDENTIFIED:")
            print(f"  Type: {planning.get('vulnerability_type')}")
            print(f"  Entry Point: {planning.get('entry_point')}")
            print(f"  Confidence: {planning.get('confidence', 0):.1%}\n")
        
        # Results
        metrics = self.report.get("metrics", {})
        if metrics:
            print("SECURITY METRICS:")
            print(f"  Before Fix: {metrics['attack_success_before']}/{metrics['attack_trials']} exploits succeeded")
            print(f"  After Fix: {metrics['attack_success_after']}/{metrics['attack_trials']} exploits succeeded")
            print(f"  Improvement: {metrics['security_improvement']:.1%}\n")
        
        # Teaching
        teaching = self.report.get("stages", {}).get("teaching", {})
        if teaching and teaching.get("questions"):
            print("LEARNING CONTENT:")
            for i, q in enumerate(teaching.get("questions", [])[:3], 1):
                print(f"  Q{i}: {q}")
            if teaching.get("hint"):
                print(f"  Hint: {teaching['hint']}\n")
        
        print("="*70 + "\n")
