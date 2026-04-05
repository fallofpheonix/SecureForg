# Sentinel-Scribe: Offline Adversarial Reasoning Engine

**Autonomous security vulnerability detection, exploitation, and remediation.**

```
LLM is NOT trusted → execution is ground truth
```

## Core Principle

Sentinel-Scribe validates all reasoning through actual code execution. The system thinks like an attacker, generates exploits, runs them in a sandbox, detects vulnerabilities, generates fixes, and validates them—all offline using Ollama + Gemma 4:e4b.

## Architecture

```
INPUT (Code)
    ↓
[1] Context Loader      (structure multi-file code)
    ↓
[2] Adversarial Planner (identify vulnerabilities via LLM reasoning)
    ↓
[3] Attack Generator    (synthesize payloads)
    ↓
[4] Sandbox Executor    (run code safely)
    ↓
[5] Exploit Detector    (measure attack success)
    ↓
[6] Patch Generator     (generate fixes)
    ↓
[7] Validation Engine   (re-test attacks on fixes)
    ↓
[8] Socratic Engine     (teach security concept)
    ↓
[9] Output + Metrics    (report findings)
```

## Data Flow

```
PLAN → ATTACK → EXECUTE → VERIFY → FIX → RE-VERIFY → TEACH
```

## Installation

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Gemma 4:e4b model available

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Ollama (in separate terminal)
ollama serve

# 3. Pull Gemma model (first time only)
ollama pull gemma4:e4b
```

## Quick Start

### Single File Analysis

```bash
python cli.py --file vulnerable_code.py
```

### Directory Analysis

```bash
python cli.py --dir ./code_samples
```

### With Custom Instruction

```bash
python cli.py --file code.py --instruction "Focus on input validation"
```

### Save Report

```bash
python cli.py --file code.py --output report.json
```

## Module Breakdown

### 1. Context Loader
- **Purpose**: Prepare structured input for LLM
- **Input**: Multiple code files
- **Output**: Formatted context string

### 2. Adversarial Planner (CORE)
- **Purpose**: Identify vulnerabilities via reasoning
- **Method**: LLM analyzes data flow from entry points to sinks
- **Output**: Attack plan with exploit strategy

### 3. Attack Generator
- **Purpose**: Convert strategy → executable payloads
- **Methods**: Original, URL-encoded, double-encoded, unicode-escaped
- **Output**: List of test payloads

### 4. Sandbox Executor
- **Purpose**: Execute untrusted code safely
- **Features**: Timeout (2s), stdout/stderr capture, temp file cleanup
- **Ground Truth**: Actual execution supersedes any analysis

### 5. Exploit Detector
- **Purpose**: Determine if attack succeeded
- **Method**: Keyword matching + pattern analysis
- **Output**: Boolean success/failure

### 6. Patch Generator
- **Purpose**: Fix vulnerability minimally
- **Method**: LLM generates unified diff
- **Output**: Patch in diff format

### 7. Validation Engine
- **Purpose**: Verify fix correctness
- **Method**: Re-run all attacks against patched code
- **Output**: Security improvement metrics

### 8. Socratic Engine
- **Purpose**: Teach security reasoning
- **Method**: Generate guiding questions, hints, explanations
- **Output**: Learning objectives

### 9. Output Layer
- **Purpose**: Display findings
- **Output**: Pretty-printed report + JSON export

## Example Walkthrough

### Vulnerable Code
```python
query = f"SELECT * FROM users WHERE id={user_input}"
```

### Pipeline Execution

```
[1] Context Load     → Code loaded (50 chars)
[2] Adversarial Plan → SQL injection identified
                        Entry point: user_input
                        Sink: SELECT query
                        Strategy: "' OR 1=1 --"
[3] Attack Gen       → 4 payloads generated
[4] Sandbox Exec     → Payload 1: "' OR 1=1 --"
[5] Exploit Detect   → Success! (contains "SELECT")
[6] Patch Gen        → Fix: use parameterized queries
[7] Validation       → Re-test: all exploits blocked ✓
[8] Teaching         → Q: How does separating data from code help?
                        Hint: Use prepared statements
[9] Metrics          → 1/1 exploits found → 0/1 after fix (100% improvement)
```

## Output Format

```
VULNERABILITY IDENTIFIED:
  Type: SQL Injection
  Entry Point: user_input
  Confidence: 85%

SECURITY METRICS:
  Before Fix: 1/1 exploits succeeded (100%)
  After Fix: 0/1 exploits succeeded (0%)
  Improvement: 100%

LEARNING CONTENT:
  Q1: Where does user input enter the code?
  Q2: Can user input change the query structure?
  Q3: How can you separate data from code?
  Hint: Use parameterized queries or prepared statements
```

## Vulnerability Detection Examples

### SQL Injection
```python
query = f"SELECT * FROM users WHERE id={user_id}"
```
**Detected**: ✓  |  **Attack**: `' OR 1=1 --`

### Command Injection
```python
result = os.system(f"ping {host}")
```
**Detected**: ✓  |  **Attack**: `; cat /etc/passwd`

### Code Injection
```python
eval(user_input)
```
**Detected**: ✓  |  **Attack**: `__import__('os').system('ls')`

## Verification Philosophy

> "LLM is NOT trusted → execution is ground truth"

Every finding is verified by:
1. Executing attack against original code
2. Observing actual output (including crashes, timeouts, errors)
3. Applying patch
4. Re-executing attack
5. Confirming vulnerability blocked

## Performance

- Single file analysis: ~30s (includes LLM reasoning + execution)
- Multi-file analysis: ~45s
- Bottleneck: LLM response time (5-15s per query)

## Limitations

- Only detects vulnerabilities expressible through code execution
- LLM reasoning quality depends on Gemma 4:e4b accuracy
- Timeout (2s) may miss slow attacks
- Patching may not be optimal (validates security, not elegance)

## Testing

```bash
# Run example
python cli.py --file examples/sql_injection_example.py

# Save report
python cli.py --file examples/sql_injection_example.py --output test_report.json

# Check Ollama
python cli.py --check-ollama
```

## System Requirements

| Component | Requirement |
|-----------|------------|
| Python | 3.8+ |
| RAM | 8GB+ (for Gemma 4:e4b) |
| Storage | 15GB (Ollama + model) |
| Network | Offline (except Ollama init) |
| CPU | 4+ cores recommended |

## Configuration

Edit `config.py`:
- `OLLAMA_MODEL`: Change model (default: gemma4:e4b)
- `SANDBOX_TIMEOUT`: Execution timeout in seconds
- `EXPLOIT_DETECTION_KEYWORDS`: Custom detection patterns

## Metrics Tracked

- Vulnerability type
- Entry point identification
- Attack payloads generated
- Original vulnerability count
- Post-patch vulnerability count
- Security improvement percentage
- Exploit blocking confirmation

## Design Principles

1. **Offline-First**: No cloud dependencies
2. **Ground Truth**: Execution > Analysis
3. **Adversarial**: Think like attacker
4. **Automated**: End-to-end without manual intervention
5. **Teaching**: Explain *why*, not just the fix
6. **Measurable**: Quantify security improvement

## Ethics

Sentinel-Scribe is designed for:
- ✓ Educational purposes
- ✓ Security training
- ✓ Penetration testing (authorized)
- ✓ Code review and hardening

NOT for:
- ✗ Unauthorized access
- ✗ Malicious exploitation
- ✗ Production attacks

## Architecture Benefits

| Layer | Benefit |
|-------|---------|
| 1. Context | Multi-file reasoning context |
| 2. Planner | Reasoned vulnerability identification |
| 3. Generator | Systematic payload synthesis |
| 4. Executor | Trusted execution validation |
| 5. Detector | Measurable success detection |
| 6. Patcher | Automated fix generation |
| 7. Validator | Regression testing |
| 8. Socratic | Educational value |
| 9. Output | Complete verification trail |

## Future Enhancements (Out of Scope)

- Support for multiple languages
- Cloud-based analysis
- Real-time monitoring
- Distributed execution
- Advanced ML-based detection

## License

Educational use only. See LICENSE file.

## Support

For issues or questions:
1. Check Ollama connection: `python cli.py --check-ollama`
2. Verify model availability: `ollama list`
3. Review example output: `python cli.py --file examples/sql_injection_example.py`

---

**Sentinel-Scribe** ≡ Offline security reasoning + verified execution
