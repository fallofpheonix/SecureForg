from core.executor import execute
from core.detector import detect_behavior_change
from core.validator import validate
from analysis.payloads import generate_payloads
from analysis.ast_analyzer import analyze_ast

def patch_code(code: str) -> str:
    # Optional logic. Real patching omitted for demo stability.
    return code

def run_pipeline(code: str) -> dict:
    # AST Check (Optional Planner Logic replacement)
    ast_plan = analyze_ast(code)

    payloads = generate_payloads()

    benign = execute(code, "1")

    results = []
    for p in payloads:
        attack = execute(code, p)
        results.append(detect_behavior_change(benign, attack))

    vulnerable = any(results)

    if not vulnerable:
        return {
            "status": "safe",
            "ast_plan": ast_plan
        }

    patched = patch_code(code)
    
    validation = validate(code, patched, payloads)

    return {
        "status": "vulnerable",
        "ast_plan": ast_plan,
        "validation": validation,
        "payloads_tested": len(payloads),
        "vulnerable_payloads": sum(results)
    }
