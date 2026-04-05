# Sentinel-Scribe

Static analyzers can miss runtime exploit behavior.
This project verifies code by executing a safe baseline and fixed attack payloads, then comparing behavior.

## Demo

```bash
pip install -r requirements.txt
python cli.py --file examples/sql_vuln.py
```

Expected shape:

```json
{
  "status": "vulnerable",
  "payloads_tested": 3,
  "vulnerable_payloads": 1
}
```

## Evaluation

```bash
python evaluate.py
```

## Comparison

| Tool | Detects runtime exploit |
| --- | --- |
| Bandit | No |
| Sentinel-Scribe | Yes |

## Boundaries

Supports:
- injection vulnerabilities
- runtime-triggerable flaws

Does not support:
- memory corruption
- multi-step exploits
- network-based attacks

## Limitations

- requires an executable path
- payload-dependent
- current detector semantics can over-report fixed code as vulnerable when attack output still differs from the benign baseline

## Structure

```text
project/
├── core/
│   ├── executor.py
│   ├── detector.py
│   ├── validator.py
├── analysis/
│   ├── payloads.py
│   ├── ast_analyzer.py
├── app/
│   ├── cli.py
│   ├── ui.py
├── examples/
│   ├── sql_vuln.py
│   ├── cmd_vuln.py
│   ├── code_vuln.py
│   ├── fixed_sql.py
├── cli.py
├── evaluate.py
├── README.md
├── requirements.txt
```
