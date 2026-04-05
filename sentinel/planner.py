from llm_safe import safe_generate

def plan_attack(context: str):
    plan = safe_generate(context)

    if not plan or "payload_hint" not in plan:
        raise RuntimeError("Planner failed")

    return plan
