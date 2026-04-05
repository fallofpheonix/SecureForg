import ollama
import subprocess
import tempfile
import os
import json

# ---------------- LLM ---------------- #

def safe_plan(prompt):
    try:
        response = ollama.generate(
            model="gemma4:4b",
            prompt=prompt
        )["response"]

        start = response.find("{")
        end = response.rfind("}") + 1
        return json.loads(response[start:end])

    except:
        return {
            "payload_hint": "' OR 1=1 --"
        }

# ---------------- EXECUTION ---------------- #

def execute(code, payload):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name

    try:
        result = subprocess.run(
            ["python3", path],
            input=payload,
            text=True,
            capture_output=True,
            timeout=3
        )

        return result.stdout

    except:
        return "ERROR"

    finally:
        os.unlink(path)

# ---------------- DETECTION ---------------- #

def detect_vuln(benign, attack):
    if "error" in attack.lower():
        return True
    if len(attack) > len(benign) * 2:
        return True
    return False

# ---------------- PATCH ---------------- #

def patch_code(code):
    # controlled demo patch
    return code.replace(
        'query = "SELECT * FROM users WHERE id=" + user_input',
        'query = "SAFE QUERY"'
    )

# ---------------- PIPELINE ---------------- #

def run():
    code = """
user_input = input()
query = "SELECT * FROM users WHERE id=" + user_input

if "OR" in query:
    print("LOGIN BYPASSED")
else:
    print("Normal User")
"""

    print("\n[STEP 1: PLAN]")
    plan = safe_plan(code)
    print(plan)

    payload = plan.get("payload_hint", "' OR 1=1 --")

    print("\n[STEP 2: BASELINE]")
    benign = execute(code, "1")
    print(benign)

    print("\n[STEP 3: ATTACK]")
    attack = execute(code, payload)
    print(attack)

    vulnerable = detect_vuln(benign, attack)
    print("Vulnerable:", vulnerable)

    if not vulnerable:
        print("No vulnerability detected.")
        return

    print("\n[STEP 4: PATCH]")
    fixed_code = patch_code(code)

    print("\n[STEP 5: RE-TEST]")
    benign_fixed = execute(fixed_code, "1")
    attack_fixed = execute(fixed_code, payload)

    print("After Fix (benign):", benign_fixed)
    print("After Fix (attack):", attack_fixed)

    fixed = not detect_vuln(benign_fixed, attack_fixed)

    print("\n[FINAL RESULT]")
    print("System Secure:", fixed)


if __name__ == "__main__":
    run()
