def detect_behavior_change(benign: dict, attack: dict) -> bool:
    """
    Behavioral diffing. Single source of truth.
    No keywords, no heuristics, no LLM.
    """
    if benign["stdout"] != attack["stdout"]:
        return True

    if "error" in attack["stderr"].lower():
        return True

    if len(attack["stdout"]) > 2 * len(benign["stdout"]):
        return True

    return False
