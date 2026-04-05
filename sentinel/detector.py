def detect_exploit(output):
    stdout = output.get("stdout", "").lower()

    if "bypass" in stdout:
        return True
    if "all users" in stdout:
        return True
    if "admin" in stdout:
        return True

    return False
