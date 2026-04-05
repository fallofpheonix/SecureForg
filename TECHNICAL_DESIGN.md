# Technical Design

## Core Loop

```
1. Plan Attack
2. Generate Payloads
3. Execute Code
4. Detect Exploit
5. Generate Patch
6. Validate Fix
7. Generate Explanation
```

---

## Components

### Adversarial Planner

* Input: full code context
* Output: vulnerability + exploit strategy

### Attack Generator

* Converts strategy into payloads

### Sandbox Executor

* Runs code in isolated environment

### Exploit Detector

* Determines attack success

### Patch Generator

* Produces secure code fix

### Validation Engine

* Re-tests system after fix

---

## Design Principles

* Execution > Prediction
* Minimal patching
* Deterministic validation
* Offline-first architecture
