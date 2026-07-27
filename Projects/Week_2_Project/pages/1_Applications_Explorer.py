import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.applications import DOMAINS, domain_names

st.set_page_config(page_title="Applications Explorer", page_icon="🌍", layout="wide")
st.title("🌍 Applications Explorer")

domain = st.selectbox("Choose a domain", domain_names())
data = DOMAINS[domain]

st.subheader("Why robots are used here")
for point in data["advantages"]:
    st.markdown(f"- {point}")

st.subheader("Tasks and examples")
for task, desc in data["tasks"].items():
    with st.expander(task):
        st.write(desc)

st.divider()
st.subheader("All domains at a glance")
for name in domain_names():
    st.markdown(f"**{name}**: " + ", ".join(DOMAINS[name]["tasks"].keys()))
