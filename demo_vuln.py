user_input = input("Enter user id: ")

# Intentional vulnerability (controlled)
query = "SELECT * FROM users WHERE id=" + user_input

# Simulated database behavior
if "OR" in query:
    print("LOGIN BYPASSED")
    print("ALL USERS DATA EXPOSED")
else:
    print("User Found: ID =", user_input)
