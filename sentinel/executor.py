import subprocess
import tempfile
import os

def execute_code(code: str, payload: str):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        file_path = f.name

    try:
        result = subprocess.run(
            ["python", file_path],
            input=payload,
            text=True,
            capture_output=True,
            timeout=2
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        os.unlink(file_path)
