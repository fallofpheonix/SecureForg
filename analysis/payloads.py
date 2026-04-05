def generate_payloads() -> list:
    """
    Deterministic payload generation logic. No LLM randomness.
    """
    return [
        "' OR 1=1 --",                           # SQL Injection
        "; ls",                                  # Command Injection
        "__import__('os').system('echo PWNED')"  # Code Injection (eval/exec)
    ]
