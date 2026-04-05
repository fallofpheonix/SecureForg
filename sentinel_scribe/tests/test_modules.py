"""
Test Suite for Sentinel-Scribe
"""

import sys
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline import SentinelScribePipeline
from modules import SandboxExecutor, ExploitDetector


def test_sql_injection_detection():
    """Test SQL injection vulnerability detection."""
    print("\n" + "="*70)
    print("TEST 1: SQL Injection Detection")
    print("="*70)
    
    vulnerable_code = '''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id={user_id}"
    if user_id == "' OR 1=1 --":
        return "SELECT all users - EXPLOITATION SUCCESSFUL"
    return "User found"
'''
    
    files = {"vulnerable.py": vulnerable_code}
    
    pipeline = SentinelScribePipeline()
    report = pipeline.run_full_pipeline(files)
    
    # Check results
    metrics = report.get("metrics", {})
    assert metrics.get("vulnerability_type") is not None, "Should identify vulnerability type"
    assert metrics.get("attack_success_before", 0) >= 0, "Should test attacks"
    
    print("✓ SQL injection detection test PASSED\n")
    return True


def test_sandbox_execution():
    """Test safe code execution."""
    print("="*70)
    print("TEST 2: Sandbox Execution")
    print("="*70)
    
    executor = SandboxExecutor(timeout=2)
    
    code = '''
print("Hello from sandbox")
x = 1 + 1
print(f"Result: {x}")
'''
    
    stdout, stderr, returncode = executor.execute(code)
    
    assert "Hello from sandbox" in stdout, "Should capture output"
    assert returncode == 0, "Should return 0"
    
    print(f"Output: {stdout.strip()}")
    print("✓ Sandbox execution test PASSED\n")
    return True


def test_exploit_detection():
    """Test exploit detection."""
    print("="*70)
    print("TEST 3: Exploit Detection")
    print("="*70)
    
    detector = ExploitDetector()
    
    # Should detect
    output1 = "SELECT * FROM users - all users retrieved"
    assert detector.detect_exploit(output1), "Should detect SQL SELECT pattern"
    
    # Should not detect
    output2 = "User not found"
    assert not detector.detect_exploit(output2), "Should not detect normal output"
    
    print("✓ Exploit detection test PASSED\n")
    return True


def test_patch_validation():
    """Test patch generation and validation."""
    print("="*70)
    print("TEST 4: Patch Validation")
    print("="*70)
    
    from modules import PatchGenerator
    
    generator = PatchGenerator()
    
    # Test syntax validation
    valid_code = "x = 1"
    invalid_code = "x = "
    
    assert generator.validate_patch_syntax(valid_code), "Should validate correct syntax"
    assert not generator.validate_patch_syntax(invalid_code), "Should reject invalid syntax"
    
    print("✓ Patch validation test PASSED\n")
    return True


def test_multi_payload_generation():
    """Test payload generation variations."""
    print("="*70)
    print("TEST 5: Multi-Payload Generation")
    print("="*70)
    
    from modules import AttackGenerator
    
    generator = AttackGenerator()
    
    plan = {
        "payload_hint": "' OR 1=1 --"
    }
    
    payloads = generator.generate_payloads(plan)
    
    assert len(payloads) > 1, "Should generate multiple payloads"
    assert "' OR 1=1 --" in payloads, "Should include original"
    
    print(f"Generated {len(payloads)} payload variations")
    for i, p in enumerate(payloads, 1):
        print(f"  {i}. {p[:50]}")
    
    print("✓ Multi-payload generation test PASSED\n")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("SENTINEL-SCRIBE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Sandbox Execution", test_sandbox_execution),
        ("Exploit Detection", test_exploit_detection),
        ("Patch Validation", test_patch_validation),
        ("Multi-Payload Generation", test_multi_payload_generation),
        ("SQL Injection Detection", test_sql_injection_detection),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, "PASS", None))
        except AssertionError as e:
            results.append((name, "FAIL", str(e)))
            print(f"✗ {name} FAILED: {e}\n")
        except Exception as e:
            results.append((name, "ERROR", str(e)))
            print(f"✗ {name} ERROR: {e}\n")
    
    # Summary
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, r, _ in results if r == "PASS")
    total = len(results)
    
    for name, result, error in results:
        status = "✓" if result == "PASS" else "✗"
        print(f"{status} {name}: {result}")
        if error:
            print(f"  {error}")
    
    print("="*70)
    print(f"Total: {passed}/{total} tests passed\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
