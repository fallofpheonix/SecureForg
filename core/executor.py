import subprocess
import tempfile
import os

EXECUTION_TIMEOUT = 2
EXECUTION_ENV = {
    "PATH": os.environ.get("PATH", ""),
    "PYTHONIOENCODING": "utf-8",
}


def execute(code: str, payload: str, timeout=2) -> dict:
    """
    Controlled subprocess execution.
    No shared globals, isolated process state, cleanup guaranteed.
    """
    with tempfile.TemporaryDirectory() as workdir:
        path = os.path.join(workdir, "target.py")
        with open(path, "w") as f:
            f.write(code)

        try:
            result = subprocess.run(
                ["python3", path],
                input=payload,
                text=True,
                capture_output=True,
                timeout=timeout,
                cwd=workdir,
                env=EXECUTION_ENV,
            )

            stderr = result.stderr.replace(path, "<target>").strip()
            return {
                "stdout": result.stdout.strip(),
                "stderr": stderr,
                "exit_code": result.returncode,
                "timeout": False,
            }

        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "TIMEOUT",
                "exit_code": -1,
                "timeout": True,
            }
        except Exception as error:
            return {
                "stdout": "",
                "stderr": f"EXECUTION_ERROR: {error}",
                "exit_code": -1,
                "timeout": False,
            }
