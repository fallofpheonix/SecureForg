import json
import shutil
import subprocess
import time
from pathlib import Path

from pipeline import run_pipeline

DATASET = [
    {
        "file": "examples/sql_vuln.py",
        "expected": "vulnerable",
        "label": "sql_injection",
    },
    {
        "file": "examples/cmd_vuln.py",
        "expected": "vulnerable",
        "label": "command_injection",
    },
    {
        "file": "examples/code_vuln.py",
        "expected": "vulnerable",
        "label": "code_injection",
    },
    {
        "file": "examples/safe.py",
        "expected": "safe",
        "label": "safe_constant",
    },
]


def load_code(path: str) -> str:
    return Path(path).read_text()


def sentinel_prediction(path: str) -> dict:
    code = load_code(path)
    start = time.perf_counter()
    report = run_pipeline(code, log_stream=None)
    elapsed = time.perf_counter() - start
    predicted = "vulnerable" if report["status"] == "vulnerable" else "safe"
    return {
        "status": report["status"],
        "predicted": predicted,
        "runtime_seconds": elapsed,
        "report": report,
    }


def run_bandit(path: str) -> dict:
    bandit_bin = shutil.which("bandit")
    if bandit_bin is None:
        return {
            "status": "unavailable",
            "predicted": "unavailable",
            "details": "bandit not installed",
        }

    result = subprocess.run(
        [bandit_bin, "-q", "-f", "json", path],
        text=True,
        capture_output=True,
        timeout=10,
    )
    if result.returncode not in (0, 1):
        return {
            "status": "error",
            "predicted": "unavailable",
            "details": result.stderr.strip() or "bandit execution failed",
        }

    payload = json.loads(result.stdout or "{}")
    issues = payload.get("results", [])
    predicted = "vulnerable" if issues else "safe"
    return {
        "status": "ok",
        "predicted": predicted,
        "details": f"issues={len(issues)}",
    }


def compute_metrics(rows: list) -> dict:
    total = len(rows)
    correct = sum(row["sentinel"]["predicted"] == row["expected"] for row in rows)
    safe_rows = [row for row in rows if row["expected"] == "safe"]
    vulnerable_rows = [row for row in rows if row["expected"] == "vulnerable"]
    safe_predicted_vulnerable = sum(
        row["sentinel"]["predicted"] == "vulnerable" for row in safe_rows
    )
    vulnerable_predicted_safe = sum(
        row["sentinel"]["predicted"] == "safe" for row in vulnerable_rows
    )
    total_runtime = sum(row["sentinel"]["runtime_seconds"] for row in rows)
    per_payload = total_runtime / (total * 3) if total else 0.0
    return {
        "accuracy": {
            "correct": correct,
            "total": total,
            "value": correct / total if total else 0.0,
        },
        "false_positive": {
            "count": safe_predicted_vulnerable,
            "total_safe": len(safe_rows),
            "value": safe_predicted_vulnerable / len(safe_rows) if safe_rows else 0.0,
        },
        "false_negative": {
            "count": vulnerable_predicted_safe,
            "total_vulnerable": len(vulnerable_rows),
            "value": vulnerable_predicted_safe / len(vulnerable_rows) if vulnerable_rows else 0.0,
        },
        "runtime": {
            "total_seconds": total_runtime,
            "per_payload_seconds": per_payload,
        },
    }


def print_summary(rows: list, metrics: dict) -> None:
    print("Running evaluation...")
    print()
    for row in rows:
        marker = "✓" if row["sentinel"]["predicted"] == row["expected"] else "x"
        print(f"{Path(row['file']).name} -> {row['sentinel']['predicted']} {marker}")
    print()
    print("Comparison")
    print("File | Expected | Sentinel | Bandit")
    print("------------------------------------")
    for row in rows:
        print(
            f"{row['file']} | {row['expected']} | "
            f"{row['sentinel']['predicted']} | {row['bandit']['predicted']}"
        )
    print()
    print(
        f"Accuracy: {metrics['accuracy']['correct']}/{metrics['accuracy']['total']} "
        f"({metrics['accuracy']['value']:.2f})"
    )
    print(
        f"False Positives: {metrics['false_positive']['count']}/{metrics['false_positive']['total_safe']} "
        f"({metrics['false_positive']['value']:.2f})"
    )
    print(
        f"False Negatives: {metrics['false_negative']['count']}/{metrics['false_negative']['total_vulnerable']} "
        f"({metrics['false_negative']['value']:.2f})"
    )
    print(
        f"Runtime: total={metrics['runtime']['total_seconds']:.3f}s "
        f"per_payload={metrics['runtime']['per_payload_seconds']:.3f}s"
    )
    print()
    print("Limitations")
    print("- Requires a payload to reach an executable path.")
    print("- Does not support memory corruption, multi-step exploits, or network attacks.")
    print("- Current detector semantics can over-report fixed code as still vulnerable when attack output differs from the benign baseline.")


def main() -> None:
    rows = []
    for entry in DATASET:
        sentinel = sentinel_prediction(entry["file"])
        bandit = run_bandit(entry["file"])
        rows.append(
            {
                "file": entry["file"],
                "label": entry["label"],
                "expected": entry["expected"],
                "sentinel": sentinel,
                "bandit": bandit,
            }
        )

    metrics = compute_metrics(rows)
    print_summary(rows, metrics)


if __name__ == "__main__":
    main()
