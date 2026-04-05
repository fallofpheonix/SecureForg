from core.executor import execute
from core.detector import detect_behavior_change

def validate(code: str, patched_code: str, payloads: list) -> dict:
    """
    Re-run + compare over patched codebase against original baseline rules.
    """
    benign_patched = execute(patched_code, "1")

    patched_results = []
    for p in payloads:
        attack = execute(patched_code, p)
        patched_results.append(detect_behavior_change(benign_patched, attack))

    patched_vulnerable = sum(patched_results)
    
    # Normally we do 'improvement' via comparing to pre-patch vulnerabilities.
    # We leave to the pipeline to calculate if it wants.
    
    return {
        "patched_vulnerable": patched_vulnerable,
        "total": len(payloads)
    }
