from core.detector import detect_behavior_change
from core.executor import execute
from analysis.payloads import SAFE_INPUT


def empty_validation(reason: str) -> dict:
    return {
        "status": "not_run",
        "reason": reason,
        "original_vulnerable": 0,
        "patched_vulnerable": 0,
        "total_payloads": 0,
        "improvement": 0.0,
        "patched_benign_output": {
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
            "timeout": False,
        },
        "patched_results": [],
        "evidence": [],
    }


def validate(patched_code: str, payloads: list, original_results: list) -> dict:
    benign_output = execute(patched_code, SAFE_INPUT)
    patched_results = []

    for original_result in original_results:
        payload = original_result["payload"]
        attack_output = execute(patched_code, payload)
        vulnerable = detect_behavior_change(benign_output, attack_output)
        patched_results.append(
            {
                "payload": payload,
                "benign_output": benign_output,
                "attack_output": attack_output,
                "vulnerable": vulnerable,
            }
        )

    original_vulnerable = sum(result["vulnerable"] for result in original_results)
    patched_vulnerable = sum(result["vulnerable"] for result in patched_results)
    total_payloads = len(payloads)
    improvement = (
        (original_vulnerable - patched_vulnerable) / total_payloads if total_payloads else 0.0
    )
    unstable_patch = benign_output["timeout"] or "error" in benign_output["stderr"].lower()

    evidence = []
    for before, after in zip(original_results, patched_results):
        before_unstable = before["attack_output"]["timeout"] or "error" in before["attack_output"]["stderr"].lower()
        after_unstable = after["attack_output"]["timeout"] or "error" in after["attack_output"]["stderr"].lower()
        if after_unstable and not before_unstable:
            unstable_patch = True

        evidence.append(
            {
                "payload": before["payload"],
                "before": before["attack_output"],
                "after": after["attack_output"],
            }
        )

    if unstable_patch:
        status = "unstable_patch"
    elif patched_vulnerable == 0:
        status = "fix_successful"
    elif patched_vulnerable < original_vulnerable:
        status = "partial_fix"
    else:
        status = "fix_failed"

    return {
        "status": status,
        "reason": "",
        "original_vulnerable": original_vulnerable,
        "patched_vulnerable": patched_vulnerable,
        "total_payloads": total_payloads,
        "improvement": improvement,
        "patched_benign_output": benign_output,
        "patched_results": patched_results,
        "evidence": evidence,
    }
