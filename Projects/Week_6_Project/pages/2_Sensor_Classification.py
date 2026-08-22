import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from core.sensors_reference import LOCATION_CLASSES, CONTACT_CLASSES, CHARACTERISTICS

st.set_page_config(page_title="Sensor Classification", page_icon="📡", layout="wide")
st.title("📡 Sensor Classification")

st.subheader("By location / purpose")
for name, desc in LOCATION_CLASSES.items():
    st.markdown(f"**{name}**: {desc}")

st.divider()
st.subheader("By contact")
for name, desc in CONTACT_CLASSES.items():
    st.markdown(f"**{name}**: {desc}")

st.divider()
st.subheader("Sensor characteristics and specifications")
for name, desc in CHARACTERISTICS.items():
    st.markdown(f"**{name}**: {desc}")
