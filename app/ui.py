import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import run_pipeline

st.set_page_config(layout="wide")

st.title("🛡️ Sentinel-Scribe: Execution Verification Engine")

uploaded = st.file_uploader("Upload Python file script", type=["py"])

if uploaded:
    code = uploaded.read().decode()
    
    st.subheader("Source Code")
    st.code(code, language="python")
    
    if st.button("Run Verification"):
        with st.spinner("Executing Deterministic Behavioral Pipeline..."):
            result = run_pipeline(code)
            
            if result["status"] == "safe":
                st.success("✅ Secure: No execution deviation detected.")
            else:
                st.error("❌ Vulnerable: Behavior change detected on attack payload!")
            
            st.json(result)
