import streamlit as st
import os
import json

st.set_page_config(page_title="Fire Alarm Trigger", layout="centered")

signal_file = "fire_signal.json"

# Load current state
if os.path.exists(signal_file):
    with open(signal_file, "r") as f:
        fire_state = json.load(f)
else:
    fire_state = {"fire": False}

trigger = st.checkbox("🔥 Trigger Fire Alarm", value=fire_state["fire"])

with open(signal_file, "w") as f:
    json.dump({"fire": trigger}, f)

if trigger:
    st.error("🚨 FIRE ALARM IS ACTIVE")
else:
    st.success("✅ System is clear")

# streamlit run fire_trigger.py --server.port 8502
