import subprocess
import tempfile
import os

def execute(code: str, payload: str, timeout=2) -> dict:
    """
    Controlled subprocess execution.
    No shared globals, isolated process state, cleanup guaranteed.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name

    try:
        result = subprocess.run(
            ["python3", path],
            input=payload,
            text=True,
            capture_output=True,
            timeout=timeout
        )

        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "TIMEOUT",
            "exit_code": -1
        }

    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
