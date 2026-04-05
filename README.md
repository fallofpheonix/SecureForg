# Sentinel-Scribe: Adversarial Reasoning Engine

## Overview

Sentinel-Scribe is an **offline autonomous system** that verifies and secures code through adversarial reasoning.

Instead of trusting AI-generated code, Sentinel-Scribe:

* Identifies vulnerabilities
* Generates real exploits
* Executes attacks
* Fixes insecure code
* Verifies the fix through re-execution
* Explains the reasoning to the developer

This transforms AI from a **code generator** into a **verified engineering system**.

---

## Core Idea

Traditional AI systems rely on:

* static analysis
* confidence scores
* self-verification

Sentinel-Scribe replaces this with:

**Execution-Grounded Verification**

```
Plan → Attack → Execute → Detect → Fix → Re-Verify → Teach
```

---

## Key Features

### 1. Adversarial Reasoning

* Thinks like an attacker
* Identifies trust boundary violations
* Generates exploit strategies

### 2. Dynamic Attack Generation

* Creates context-aware payloads
* Executes real attacks in sandbox

### 3. Execution-Based Validation

* Uses runtime behavior as ground truth
* No reliance on LLM confidence

### 4. Automatic Secure Repair

* Fixes vulnerabilities using secure coding practices
* Preserves original functionality

### 5. Re-Attack Verification

* Confirms exploit is fully mitigated
* Provides measurable security proof

### 6. Socratic Teaching Layer

* Explains vulnerabilities
* Guides developer reasoning

---

## Architecture

```
Input Code
 ↓
Context Loader
 ↓
Adversarial Planner
 ↓
Attack Generator
 ↓
Sandbox Executor
 ↓
Exploit Detector
 ↓
Patch Generator
 ↓
Validation Engine
 ↓
Socratic Engine
 ↓
Output + UI
```

---

## Example Flow

### Vulnerable Code

```python
query = "SELECT * FROM users WHERE id=" + user_input
```

### Attack

```
Payload: ' OR 1=1 --
Result: LOGIN BYPASSED
```

### Fix

```python
query = "SELECT * FROM users WHERE id=%s"
cursor.execute(query, (user_input,))
```

### Verification

```
Payload: ' OR 1=1 --
Result: Blocked
```

---

## Installation

```bash
pip install ollama streamlit
ollama pull gemma4:e4b
```

---

## Usage

### CLI

```bash
python main.py
```

### UI

```bash
streamlit run app.py
```

---

## Project Structure

```
sentinel_scribe/
├── modules/
│   ├── context_loader.py
│   ├── adversarial_planner.py
│   ├── attack_generator.py
│   ├── sandbox_executor.py
│   ├── exploit_detector.py
│   ├── patch_generator.py
│   ├── validation_engine.py
│   ├── socratic_engine.py
│
├── pipeline.py
├── cli.py
├── utils.py
```

---

## Metrics

* Attack Success Rate (Before Fix)
* Attack Block Rate (After Fix)
* Security Improvement Score
* Execution Time

---

## Use Cases

* Secure AI-generated code
* Offline development environments
* Educational security training
* Critical infrastructure systems

---

## Limitations

* Currently supports single vulnerability type (injection)
* Heuristic-based exploit detection
* Patch generation may need refinement

---

## Future Work

* Multi-vulnerability support
* AST-based patching
* Advanced fuzzing
* Semantic exploit detection

---

## License

MIT License
