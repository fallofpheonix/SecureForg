import ollama
import json

PLANNER_PROMPT = """
You are an adversarial security analyst.

Analyze the codebase below and find ONE vulnerability.

Steps:
1. Identify where user input enters
2. Trace it to a dangerous sink
3. Identify vulnerability
4. Propose exploit strategy

Output ONLY JSON:

{
  "entry_point": "...",
  "data_flow": ["..."],
  "sink": "...",
  "vulnerability_type": "injection",
  "exploit_strategy": "...",
  "payload_hint": "..."
}
"""

def extract_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])

def plan_attack(context: str):
    response = ollama.generate(
        model="gemma4:e4b",
        prompt=PLANNER_PROMPT + context
    )
    return extract_json(response["response"])
