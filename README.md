# Sentinel-Scribe: Execution-Grounded Verification Engine

## Overview

Sentinel-Scribe is an **offline autonomous engine** that verifies and secures logic through strict execution-grounded reasoning. It is designed around local reliability, fully omitting nondeterministic LLM APIs in structural verification routes.

Instead of trusting keyword or confidence-weighted scores, Sentinel-Scribe proves incorrectness through pure behavioral analysis.

---

## Core System Boundaries

```text
Input source
 ↓
Deterministic Payload Matrix (SQLi, CMDi, Eval) + Static AST Safety Net
 ↓
Process Safebox (Baseline)
 ↓
Process Safebox (Attack Sequence)
 ↓
Behavioral Delta Inspector
 ↓
Deterministic Vulnerability Score
```

---

## System Proofing Rules

1. **No External LLM Failure Points**: Operation runs 100% offline via native `subprocess` and `ast`.
2. **Behavioral Integrity**: Code vulnerabilities are matched _exclusively_ based on output behavioral deltas generated against benign execution loops.
3. **Factual Exploitation Surfaces**: Uses non-mocked data schemas (`demo/` evaluates real SQLite in-memory).

---

## Installation

```bash
pip install streamlit
```

---

## Usage

### CLI

The single required entry point parses a file target parameter.

```bash
python app/cli.py --file demo/sql_injection.py
```

### UI

Streamlit executes the visualization.

```bash
streamlit run app/ui.py
```

---

## Project Structure

```text
app/
├── cli.py
├── ui.py
analysis/
├── ast_analyzer.py
├── payloads.py
core/
├── executor.py
├── detector.py
├── validator.py
demo/
├── command_injection.py
├── sql_injection.py
├── code_injection.py
pipeline.py
```
