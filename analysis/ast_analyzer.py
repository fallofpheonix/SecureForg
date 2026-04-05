import ast

DEFAULT_ANALYSIS = {
    "type": "none",
    "confidence": "low (static heuristic)",
    "source": "ast",
}


def analyze_ast(code: str) -> dict:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {
            "type": "none",
            "confidence": "low (static heuristic)",
            "source": "ast",
        }

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
            return {
                "type": "code_injection",
                "confidence": "low (static heuristic)",
                "source": "ast",
            }

        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr == "system"
        ):
            return {
                "type": "command_injection",
                "confidence": "low (static heuristic)",
                "source": "ast",
            }

    for node in ast.walk(tree):
        if not isinstance(node, ast.BinOp) or not isinstance(node.op, ast.Add):
            continue

        left = getattr(node.left, "value", None)
        right = getattr(node.right, "value", None)
        values = [value for value in (left, right) if isinstance(value, str)]
        for value in values:
            upper = value.upper()
            if "SELECT" in upper or "INSERT" in upper or "UPDATE" in upper:
                return {
                    "type": "sql_injection",
                    "confidence": "low (static heuristic)",
                    "source": "ast",
                }

    return dict(DEFAULT_ANALYSIS)
