# Technical Design

## Core Loop

```text
input code
-> generate static payloads
-> execute benign baseline
-> execute attack
-> compare stdout/stderr/exit_code exactly
-> report vulnerability
```

## Components

### Executor

* **Input**: Python code string and stdin payload
* **Output**: dictionary `{stdout, stderr, exit_code}`
* Runs the target in a fresh subprocess from a temporary file

### Behavioral Diff Detector

* No regex, keywords, scoring, or model inference
* Reports a change iff any of `stdout`, `stderr`, or `exit_code` differs from baseline

### Payload Generator

* Returns a fixed ordered payload set
* Current categories: SQL injection, command injection, code injection
