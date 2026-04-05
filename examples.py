"""
Quick Start Guide for Sentinel-Scribe

This file demonstrates how to use the system programmatically
"""

import sys
from pathlib import Path

# Add module to path
sys.path.insert(0, str(Path(__file__).parent / "sentinel_scribe"))

from pipeline import SentinelScribePipeline


def example_1_single_file():
    """Example 1: Analyze a single vulnerable file."""
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Single File Analysis")
    print("="*70 + "\n")
    
    # Vulnerable code
    code = '''
def search_user(username):
    """Vulnerable to command injection."""
    import os
    command = f"grep {username} /etc/passwd"
    result = os.system(command)
    return result
'''
    
    files = {"vulnerable.py": code}
    
    # Run pipeline
    pipeline = SentinelScribePipeline()
    report = pipeline.run_full_pipeline(files)
    
    # Display report
    pipeline.print_report()
    
    return report


def example_2_with_instruction():
    """Example 2: Analysis with custom instruction."""
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Analysis with Custom Instruction")
    print("="*70 + "\n")
    
    code = '''
def validate_user(user_input):
    """Check if input matches pattern."""
    import re
    if re.search(user_input, "admin user"):
        return True
    return False
'''
    
    files = {"regex_code.py": code}
    instruction = "Focus on regex denial-of-service vulnerabilities"
    
    # Run pipeline
    pipeline = SentinelScribePipeline()
    report = pipeline.run_full_pipeline(files, instruction)
    
    # Display report
    pipeline.print_report()
    
    return report


def example_3_multi_file():
    """Example 3: Multi-file analysis."""
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-File Analysis")
    print("="*70 + "\n")
    
    # Multiple files
    files = {
        "auth.py": '''
def authenticate(username, password):
    """Check credentials."""
    query = f"SELECT * FROM users WHERE name='{username}' AND pass='{password}'"
    # Vulnerable to SQL injection
    return execute_query(query)
''',
        "main.py": '''
from auth import authenticate

user = input("Username: ")
pwd = input("Password: ")

if authenticate(user, pwd):
    print("Access granted")
else:
    print("Access denied")
'''
    }
    
    # Run pipeline
    pipeline = SentinelScribePipeline()
    report = pipeline.run_full_pipeline(files)
    
    # Display report
    pipeline.print_report()
    
    return report


def example_4_programmatic_access():
    """Example 4: Programmatic use of modules."""
    
    print("\n" + "="*70)
    print("EXAMPLE 4: Direct Module Access")
    print("="*70 + "\n")
    
    from modules import (
        ContextLoader,
        SandboxExecutor,
        ExploitDetector
    )
    
    # Step 1: Load context
    loader = ContextLoader()
    code = 'x = int(input())'
    context = loader.load_files({"test.py": code})
    print(f"1. Loaded context ({len(context)} chars)")
    
    # Step 2: Execute code
    executor = SandboxExecutor()
    stdout, stderr, rc = executor.execute('print("Hello World")')
    print(f"2. Executed code: {stdout.strip()}")
    
    # Step 3: Detect exploit
    detector = ExploitDetector()
    is_exploit = detector.detect_exploit("SELECT * FROM users")
    print(f"3. Detected exploit: {is_exploit}")


if __name__ == "__main__":
    
    # Run all examples
    print("\n" + "█"*70)
    print("SENTINEL-SCRIBE QUICK START EXAMPLES")
    print("█"*70)
    
    try:
        # Uncomment examples to run
        
        # example_1_single_file()
        # example_2_with_instruction()
        # example_3_multi_file()
        example_4_programmatic_access()
        
        print("\n" + "█"*70)
        print("Examples completed!")
        print("█"*70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
