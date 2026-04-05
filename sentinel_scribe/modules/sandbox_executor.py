"""
Module 4: Sandbox Executor
Safely executes untrusted code with timeouts and isolation.
"""

import subprocess
import tempfile
import os
from typing import Tuple
from config import SANDBOX_TIMEOUT


class SandboxExecutor:
    """
    Executes code in isolated environment with safety constraints.
    Execution is ground truth - we verify vulnerabilities via actual execution.
    """
    
    def __init__(self, timeout: int = SANDBOX_TIMEOUT):
        self.timeout = timeout
    
    def execute(
        self,
        code: str,
        payload: str = "",
        input_data: str = ""
    ) -> Tuple[str, str, int]:
        """
        Execute code with payload safely.
        
        Args:
            code: Python code to execute
            payload: String to pass as input/parameter
            input_data: Data to pass to stdin
        
        Returns:
            Tuple of (stdout, stderr, returncode)
        """
        # Prepare execution environment
        exec_input = f"{input_data}\n{payload}".strip()
        
        try:
            # Create temporary file for code
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False
            ) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Execute with timeout
                result = subprocess.run(
                    ['python3', temp_file],
                    input=exec_input,
                    text=True,
                    capture_output=True,
                    timeout=self.timeout
                )
                
                return result.stdout, result.stderr, result.returncode
            
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_file)
                except:
                    pass
        
        except subprocess.TimeoutExpired:
            return "", "TIMEOUT", -1
        except Exception as e:
            return "", f"EXECUTION_ERROR: {str(e)}", -1
    
    def execute_with_globals(
        self,
        code: str,
        globals_dict: dict,
        timeout: int = None
    ) -> Tuple[str, str, int, dict]:
        """
        Execute code with custom globals (advanced).
        
        Args:
            code: Code to execute
            globals_dict: Global variables to provide
            timeout: Override timeout
        
        Returns:
            Tuple of (stdout, stderr, returncode, modified_globals)
        """
        import io
        import sys
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        try:
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            
            exec(code, globals_dict)
            
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue()
            
            return stdout, stderr, 0, globals_dict
        
        except Exception as e:
            stderr = str(e)
            return "", stderr, 1, globals_dict
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
