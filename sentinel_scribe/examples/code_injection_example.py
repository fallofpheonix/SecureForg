"""
Code Injection Vulnerable Example
"""


def execute_calculation(expression):
    """Vulnerable: evaluates user input as code."""
    
    # VULNERABLE: code injection via eval()
    try:
        result = eval(expression)
        return result
    except:
        return "Error"


def process_user_function(func_string):
    """Another vulnerable pattern: exec()"""
    
    namespace = {}
    
    # VULNERABLE: exec with user input
    exec(func_string, namespace)
    
    return namespace.get('result', None)


if __name__ == "__main__":
    # Normal usage
    print("Test 1: Normal calculation")
    print(execute_calculation("2 + 2"))
    print()
    
    # Injection attempt
    print("Test 2: Code Injection Attempt")
    result = execute_calculation("__import__('os').system('echo EXPLOITATION SUCCESSFUL')")
    print(result)
