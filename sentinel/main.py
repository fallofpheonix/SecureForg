from planner import plan_attack
from attack import generate_payloads
from executor import execute_code
from detector import detect_exploit
from utils import build_context

def run():
    # Demo vulnerable system
    files = {
        "main.py": """
user_input = input("Enter ID: ")
query = "SELECT * FROM users WHERE id=" + user_input
print("Executing:", query)
if "OR" in query:
    print("LOGIN BYPASSED")
""",
    }

    # Step 1: Build context
    context = build_context(files)

    # Step 2: Plan attack
    plan = plan_attack(context)
    print("\n[PLAN]")
    print(plan)

    # Step 3: Generate payloads
    payloads = generate_payloads(plan)

    # Step 4: Execute attacks
    print("\n[ATTACK RESULTS]")
    for payload in payloads:
        output = execute_code(files["main.py"], payload)
        success = detect_exploit(output)

        print(f"\nPayload: {payload}")
        print("Output:", output["stdout"])
        print("Exploit Success:", success)

if __name__ == "__main__":
    run()
