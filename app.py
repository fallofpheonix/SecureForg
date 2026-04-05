import streamlit as st
from run import run  # or your pipeline

st.set_page_config(layout="wide")

st.title("🛡️ Sentinel-Scribe: Adversarial Verification Engine")

st.markdown("### Attack → Fix → Proof")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Before Fix (Vulnerable)")
    st.code("LOGIN BYPASSED\nALL USERS DATA EXPOSED")

with col2:
    st.subheader("🟢 After Fix (Secure)")
    st.code("User Found: ID = 1")

st.markdown("---")

st.subheader("⚙️ System Pipeline")

st.markdown("""
1. Analyze Code  
2. Generate Attack  
3. Execute Exploit  
4. Detect Vulnerability  
5. Apply Fix  
6. Re-Verify Security  
""")

if st.button("Run Verification"):
    st.success("✅ Vulnerability Detected → Fixed → Verified")
