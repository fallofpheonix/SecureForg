"""
SQL Injection Vulnerable Example
Demo code with SQL injection vulnerability for testing.
"""


def get_user(user_id):
    """Vulnerable: builds SQL query with string concatenation."""
    
    # Simulated database
    users = {
        "1": "Alice",
        "2": "Bob",
        "3": "Charlie"
    }
    
    # VULNERABLE: SQL injection risk
    query = f"SELECT * FROM users WHERE id={user_id}"
    
    print(f"Query: {query}")
    
    # Simulate query execution
    if user_id == "' OR 1=1 --":
        return "SELECT all users - EXPLOITATION SUCCESSFUL"
    elif user_id in users:
        return f"User: {users[user_id]}"
    else:
        return "User not found"


if __name__ == "__main__":
    # Test with normal ID
    print("Test 1: Normal ID")
    print(get_user("1"))
    print()
    
    # Test with injection
    print("Test 2: SQL Injection Attempt")
    result = get_user("' OR 1=1 --")
    print(result)
