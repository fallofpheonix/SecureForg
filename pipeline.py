import sys
import ast

from core.executor import execute
from core.detector import detect_behavior_change
from core.validator import empty_validation, validate
from analysis.ast_analyzer import analyze_ast
from analysis.payloads import SAFE_INPUT, generate_payloads

MAX_CODE_SIZE = 50 * 1024

def build_explanation(status: str, analysis: dict, reason: str) -> str:
    if status == "error":
        return f"Verification failed explicitly: {reason}."

    if reason == "timeout detected":
        return "Execution timed out during verification. Timeout is treated as suspicious behavior."

    if status == "vulnerable":
        if analysis["type"] == "none":
            return "Detected behavioral deviation between safe and attack input. Static analysis found no matching risk pattern."
        return (
            "Detected behavioral deviation between safe and attack input. "
            f"Possible cause: {analysis['type']} pattern identified by AST."
        )

    if status == "suspicious":
        return (
            "No runtime behavioral deviation detected for the tested payloads. "
            f"Static analysis indicates possible {analysis['type']} risk."
        )

    return "No runtime behavioral deviation detected and static analysis found no matching risk pattern."


def build_debug_trace(analysis: dict, results: list) -> list:
    trace = []
    for result in results:
        if result["attack_output"]["timeout"]:
            reason = "timeout"
        elif result["benign_output"]["stdout"] != result["attack_output"]["stdout"]:
            reason = "output difference"
        elif "error" in result["attack_output"]["stderr"].lower():
            reason = "error signal"
        elif len(result["attack_output"]["stdout"]) > 2 * len(result["benign_output"]["stdout"]):
            reason = "output size anomaly"
        else:
            reason = "no behavioral deviation"

        trace.append(
            {
                "ast_detected": analysis["type"],
                "payload_triggered": result["payload"],
                "reason": reason,
            }
        )
    return trace


def emit_log(log_stream, message: str) -> None:
    if log_stream is None:
        return
    print(message, file=log_stream)


def resolve_status(analysis: dict, benign: dict, results: list, vulnerable_payloads: int) -> tuple[str, str]:
    if benign["timeout"] or any(result["attack_output"]["timeout"] for result in results):
        return "suspicious", "timeout detected"

    if benign["exit_code"] != 0 and "error" in benign["stderr"].lower():
        return "error", "execution failed"

    if vulnerable_payloads:
        return "vulnerable", "behavioral deviation detected"

    if analysis["type"] != "none":
        return "suspicious", "static risk without runtime trigger"

    return "safe", "no behavioral deviation detected"


def collect_results(code: str, payloads: list, progress_callback=None, log_stream=None) -> tuple[dict, list]:
    benign = execute(code, SAFE_INPUT)
    results = []

    for index, payload in enumerate(payloads, start=1):
        emit_log(log_stream, f"[EXEC] payload={payload}")
        if progress_callback is not None:
            progress_callback(index, len(payloads), payload)

        attack = execute(code, payload)
        is_vulnerable = detect_behavior_change(benign, attack)
        emit_log(log_stream, f"[OUT] stdout={attack['stdout']!r} stderr={attack['stderr']!r} exit_code={attack['exit_code']} timeout={attack['timeout']}")
        emit_log(log_stream, f"[RESULT] vulnerable={is_vulnerable}")
        results.append(
            {
                "payload": payload,
                "benign_output": benign,
                "attack_output": attack,
                "vulnerable": is_vulnerable,
            }
        )

    return benign, results


def default_execution() -> dict:
    return {
        "safe_input": SAFE_INPUT,
        "benign_output": {
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
            "timeout": False,
        },
        "payloads_tested": 0,
        "vulnerable_payloads": 0,
    }


def default_analysis() -> dict:
    return {
        "type": "none",
        "confidence": "low (static heuristic)",
        "source": "ast",
    }


def error_report(reason: str) -> dict:
    analysis = default_analysis()
    execution = default_execution()
    return {
        "status": "error",
        "reason": reason,
        "analysis": analysis,
        "explanation": build_explanation("error", analysis, reason),
        "execution": execution,
        "results": [],
        "debug_trace": [],
        "validation": empty_validation("validation not run"),
    }


def validate_code_input(code: str) -> str | None:
    if len(code.encode("utf-8")) > MAX_CODE_SIZE:
        return f"input exceeds max size of {MAX_CODE_SIZE} bytes"

    try:
        ast.parse(code)
    except SyntaxError as error:
        return f"invalid python syntax: {error}"

    return None


def run_pipeline(code: str, patched_code: str | None = None, progress_callback=None, log_stream=sys.stderr) -> dict:
    input_error = validate_code_input(code)
    if input_error is not None:
        return error_report(input_error)

    patched_error = None
    if patched_code is not None:
        patched_error = validate_code_input(patched_code)

    analysis = analyze_ast(code)
    payloads = generate_payloads()
    benign, results = collect_results(
        code,
        payloads,
        progress_callback=progress_callback,
        log_stream=log_stream,
    )
    vulnerable_payloads = sum(result["vulnerable"] for result in results)
    status, reason = resolve_status(analysis, benign, results, vulnerable_payloads)

    report = {
        "status": status,
        "reason": reason,
        "analysis": analysis,
        "explanation": build_explanation(status, analysis, reason),
        "execution": {
            "safe_input": SAFE_INPUT,
            "benign_output": benign,
            "payloads_tested": len(payloads),
            "vulnerable_payloads": vulnerable_payloads,
        },
        "results": results,
        "debug_trace": build_debug_trace(analysis, results),
        "validation": empty_validation("validation not requested"),
    }

    if patched_code is not None:
        if patched_error is not None:
            report["validation"] = empty_validation(patched_error)
        else:
            report["validation"] = validate(patched_code, payloads, results)

    return report
