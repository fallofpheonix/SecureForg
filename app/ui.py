import os
import sys
from pathlib import Path

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.validator import empty_validation
from pipeline import default_analysis, default_execution, run_pipeline

DEMO_FILES = {
    "SQL Injection": Path("demo/sql_injection.py"),
    "Command Injection": Path("demo/command_injection.py"),
    "Code Injection": Path("demo/code_injection.py"),
}

PATCH_FILES = {
    "None": None,
    "SQL Injection Fixed": Path("demo/sql_injection_fixed.py"),
}


def load_text(path: Path | None) -> str | None:
    if path is None:
        return None
    return path.read_text()


def error_result(reason: str) -> dict:
    return {
        "status": "error",
        "reason": reason,
        "analysis": default_analysis(),
        "explanation": reason,
        "execution": default_execution(),
        "results": [],
        "debug_trace": [],
        "validation": empty_validation("validation not run"),
    }


st.set_page_config(page_title="Sentinel-Scribe", layout="wide")
st.title("Execution-based verification")

if "selected_code" not in st.session_state:
    st.session_state.selected_code = None
if "selected_name" not in st.session_state:
    st.session_state.selected_name = None

st.subheader("Preloaded Demos")
demo_columns = st.columns(len(DEMO_FILES))
for column, (label, path) in zip(demo_columns, DEMO_FILES.items()):
    if column.button(label, use_container_width=True):
        st.session_state.selected_name = label
        st.session_state.selected_code = path.read_text()

uploaded = st.file_uploader("Upload Python file", type=["py"])
if uploaded is not None:
    try:
        st.session_state.selected_name = uploaded.name
        st.session_state.selected_code = uploaded.read().decode()
    except Exception as error:
        st.session_state.selected_name = uploaded.name
        st.session_state.selected_code = None
        st.error(f"Failed to decode upload: {error}")

code = st.session_state.selected_code
if code is None:
    st.info("Load a preloaded demo or upload a Python file.")
    st.stop()

st.subheader("Source Code")
st.caption(st.session_state.selected_name or "Uploaded file")
st.code(code, language="python")

patch_name = st.selectbox("Patched file for validation", list(PATCH_FILES.keys()))
patched_code = load_text(PATCH_FILES[patch_name])

progress_text = st.empty()


def update_progress(index: int, total: int, payload: str) -> None:
    progress_text.write(f"Running payload {index}/{total}: {payload}")


if st.button("Run Verification", use_container_width=True):
    with st.spinner("Executing pipeline..."):
        try:
            result = run_pipeline(
                code,
                patched_code=patched_code,
                progress_callback=update_progress,
                log_stream=None,
            )
        except Exception as error:
            result = error_result(f"pipeline exception: {error}")
    progress_text.empty()

    st.subheader("Summary")
    st.json(
        {
            "status": result["status"],
            "reason": result["reason"],
            "triggered": f'{result["vulnerable_payloads"]}/{result["payloads_tested"]}',
            "analysis": result["analysis"],
        }
    )

    st.subheader("Execution")
    st.json(result["execution"])

    st.subheader("Results")
    for entry in result["results"]:
        st.json(entry)

    st.subheader("Debug Trace")
    st.json(result["debug_trace"])

    if "validation" in result:
        st.subheader("Validation")
        st.json(result["validation"])
