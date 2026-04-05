# Technical Design

## Core Loop

```text
input code
→ generate static payloads
→ execute benign baseline
→ execute attack
→ compare outputs behaviorally (diff)
→ report vulnerability
```

---

## Components

### Sandbox Executor
* **Input**: Python code string and stdin payload
* **Output**: Pure dictionary `{stdout, stderr, exit_code}`
* Runs strictly configured `subprocess.run()` logic over temp filesystem writes to ensure strict timeout safety parameters are met locally.

### Behavioral Output Detector
* Does **not** employ any regex, JSON, heuristic tracking or logic loops.
* **Logic**: Evaluates whether `attack["stdout"] != benign["stdout"]`, whether there is a crash in standard error, or a massive jump in data size.

### Analysis & Payloads Stage
* Returns static payload test sets.
* Returns AST (Abstract Syntax Tree) string tracking for fallback safety scanning exclusively (not relying on API endpoints).
