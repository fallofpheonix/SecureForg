import subprocess
import tempfile
import os

def execute_code(code: str, payload: str, timeout=3):
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
            "stdout": result.stdout,
            "stderr": result.stderr,
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
        except:
            pass
