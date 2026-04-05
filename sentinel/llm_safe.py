import ollama
import json

def safe_generate(prompt, timeout=5):
    try:
        response = ollama.generate(
            model="gemma4:4b",
            prompt=prompt,
            options={"timeout": timeout}
        )

        return extract_json_safe(response["response"])

    except Exception:
        return fallback_plan()


def extract_json_safe(text):
    try:
        return json.loads(text.strip())
    except:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
    raise ValueError("Invalid JSON")


def fallback_plan():
    return {
        "entry_point": "input",
        "sink": "query",
        "vulnerability_type": "injection",
        "payload_hint": "' OR 1=1 --"
    }
