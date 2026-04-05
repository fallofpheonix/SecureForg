"""
Command Injection Vulnerable Example
"""


def ping_host(hostname):
    """Vulnerable: passes user input directly to system command."""
    import os
    
    # VULNERABLE: command injection
    command = f"ping -c 1 {hostname}"
    result = os.system(command)
    
    if result == 0:
        print(f"Host {hostname} is reachable")
    else:
        print(f"Host {hostname} is unreachable")
    
    return result


if __name__ == "__main__":
    # Normal usage
    print("Test 1: Normal hostname")
    ping_host("google.com")
    print()
    
    # Injection attempt
    print("Test 2: Command Injection Attempt")
    result = ping_host("; echo 'COMMAND INJECTION SUCCESSFUL'")
    print(result)
