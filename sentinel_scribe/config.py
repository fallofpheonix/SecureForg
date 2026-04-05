"""
Configuration and constants for Sentinel-Scribe system.
"""

# Ollama Configuration
OLLAMA_MODEL = "gemma4:e4b"
OLLAMA_ENDPOINT = "http://localhost:11434"

# Execution Configuration
SANDBOX_TIMEOUT = 2
MAX_PAYLOAD_LENGTH = 1024
MAX_RETRIES = 3

# Detection Keywords
EXPLOIT_DETECTION_KEYWORDS = [
    "bypass",
    "all users",
    "unauthorized",
    "privilege",
    "admin",
    "select \\*",
    "drop table",
    "exec",
    "eval"
]

# System Prompts
PLANNER_PROMPT_TEMPLATE = """You are a security vulnerability analyzer. Analyze the provided code for security vulnerabilities.

Instructions:
1. Identify entry points where untrusted input enters
2. Trace data flow to sinks (database, command execution, etc.)
3. Determine vulnerability type (injection, XSS, XXE, etc.)
4. Propose exploit strategy
5. Suggest test payload

RESPOND IN VALID JSON ONLY (no markdown, no explanation):
{{
  "entry_point": "function_name",
  "data_flow": ["step1", "step2"],
  "sink": "vulnerable_operation",
  "vulnerability_type": "type_name",
  "exploit_strategy": "detailed_attack_plan",
  "payload_hint": "sample_payload",
  "confidence": 0.0
}}

CODE TO ANALYZE:
"""

PATCH_PROMPT_TEMPLATE = """You are a secure coding expert. Fix the vulnerability.

Vulnerability: {vulnerability_type}
Exploit Strategy: {exploit_strategy}

RESPOND WITH UNIFIED DIFF ONLY (no explanation):

--- original
+++ fixed
"""

SOCRATIC_PROMPT_TEMPLATE = """You are a security educator teaching via Socratic method.

Given this vulnerability: {vulnerability_type}
In this code: {code_snippet}

Generate:
1. Three guiding questions (do NOT reveal the answer)
2. A one-line hint
3. A 3-sentence explanation of the concept

Format:
QUESTIONS:
- ?
- ?
- ?

HINT:

EXPLANATION:
"""

# Metrics
METRICS_TEMPLATE = {
    "vulnerability_type": None,
    "entry_point": None,
    "attack_success_before": 0,
    "attack_trials_before": 0,
    "attack_success_after": 0,
    "attack_trials_after": 0,
    "security_improvement": 0.0,
    "exploit_payloads": [],
    "patch_applied": False
}
