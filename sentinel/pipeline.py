from planner import plan_attack
from attack import generate_payloads
from executor import execute_code
from exploit_detector import detect_behavior_change
from patch_validator import validate_patch

def run_pipeline(code: str):

    # Step 1: Plan
    plan = plan_attack(code)

    # Step 2: Generate payloads
    payloads = generate_payloads(plan)

    # Step 3: Baseline execution
    benign = execute_code(code, "1")

    if not benign:
        raise RuntimeError("Baseline execution failed")

    results = []

    for payload in payloads:
        attack = execute_code(code, payload)

        is_vuln = detect_behavior_change(benign, attack)

        results.append({
            "payload": payload,
            "output": attack,
            "vulnerable": is_vuln
        })

    # Step 4: Check if vulnerability exists
    if not any(r["vulnerable"] for r in results):
        return {"status": "no_vulnerability"}

    # Step 5: Patch (stub for now)
    patched_code = code.replace("+ user_input", ", user_input")

    validate_patch(code, patched_code)

    # Step 6: Re-test
    benign_fixed = execute_code(patched_code, "1")

    fixed_results = []
    for payload in payloads:
        attack = execute_code(patched_code, payload)
        is_vuln = detect_behavior_change(benign_fixed, attack)
        fixed_results.append(is_vuln)

    return {
        "status": "fixed",
        "before": results,
        "after": fixed_results
    }
