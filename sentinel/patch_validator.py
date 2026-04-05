def validate_patch(original_code, patched_code):
    if patched_code == original_code:
        raise RuntimeError("Patch did not modify code")

    try:
        compile(patched_code, "<patched>", "exec")
    except Exception:
        raise RuntimeError("Patched code invalid")

    return True
