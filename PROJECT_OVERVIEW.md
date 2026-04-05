# Sentinel-Scribe: Phase 0 Overview

## Scope

Sentinel-Scribe is a deterministic local verifier. It executes a Python file with a benign input and a fixed adversarial payload set, then reports whether process behavior changed.

## Included

* deterministic payload generation
* baseline execution
* attack execution
* exact diff on `stdout`, `stderr`, `exit_code`

## Excluded

* LLM planning
* patch generation
* scoring
* heuristics
* fake exploit simulation

## Architecture

```text
code input
-> deterministic payload generator
-> benign execution
-> attack execution
-> behavioral diff
-> report
```

## Phase 0 Constraints

* offline only
* single entry point: `app/cli.py`
* real execution surfaces in `demo/`
* same input yields same output
* report depends only on observed behavior change

## Evaluation Boundary

Supports:
* injection vulnerabilities
* runtime-triggerable flaws

Does not support:
* memory corruption
* multi-step exploits
* network-based attacks
