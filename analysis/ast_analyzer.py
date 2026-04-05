import ast

def analyze_ast(code: str) -> dict:
    """
    Minimal AST fallback. Detects ONLY:
    1. eval()
    2. exec()
    3. os.system(user_input)
    4. string concatenation in SQL
    
    Returns plan format identical to LLM output structure if vulnerability found.
    """
    try:
        tree = ast.parse(code)
    except Exception:
        return {"error": "Failed to parse code"}

    for node in ast.walk(tree):
        # 1 & 2: eval() and exec()
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ["eval", "exec"]:
                    return {"vulnerability_type": f"{node.func.id} injection"}
            
            # 3: os.system()
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    if node.func.attr == "system":
                        return {"vulnerability_type": "Command injection"}
                        
        # 4: String concatenation (could mean SQLi if passed to execute)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            # Extremely naive fallback: string addition is flagged as potential injection
            if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                if "SELECT" in node.left.value.upper() or "INSERT" in node.left.value.upper():
                    return {"vulnerability_type": "SQL injection"}
            if isinstance(node.right, ast.Constant) and isinstance(node.right.value, str):
                if "SELECT" in node.right.value.upper() or "INSERT" in node.right.value.upper():
                    return {"vulnerability_type": "SQL injection"}

    return {"status": "AST found no vulnerabilities"}
