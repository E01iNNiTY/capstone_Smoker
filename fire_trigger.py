import streamlit as st
import os
import json
import random

# --- Basic Setup ---
st.set_page_config(page_title="🔥 Smart Fire Simulation", layout="centered")

signal_file = "fire_signal.json"

default_state = {
    "fire": False,
    "heat": 0,
    "smoke": 0,
    "chemicals": 0
}

# --- Load Current Sensor State ---
if os.path.exists(signal_file):
    try:
        with open(signal_file, "r") as f:
            fire_state = json.load(f)
    except json.JSONDecodeError:
        fire_state = default_state.copy()
else:
    fire_state = default_state.copy()

# Make sure all keys exist
for key in default_state:
    fire_state.setdefault(key, default_state[key])

# --- Simulate Sensor Changes (Random Buildup) ---
if random.random() < 0.5:
    fire_state["heat"] += random.randint(0, 2)
if random.random() < 0.7:
    fire_state["smoke"] += random.randint(1, 3)
if random.random() < 0.3:
    fire_state["chemicals"] += random.randint(0, 5)

# --- Title ---
st.title("🔥 Smart Fire System Simulation")
st.write("Simulating real-time heat, smoke, and chemical sensor readings...")

# --- Manual Fire Trigger ---
manual_trigger = st.checkbox("🔥 Manually Trigger Fire Alarm", value=fire_state["fire"])
fire_state["fire"] = manual_trigger

# --- Helper Function: Color by Level ---
def get_color(level):
    if level < 40:
        return "green"
    elif level < 70:
        return "yellow"
    else:
        return "red"

# --- Show Sensor Readings (with color coding) ---
st.subheader("🌡️ Heat Sensor")
st.markdown(f"<div style='background-color:{get_color(fire_state['heat'])}; padding:8px; border-radius:6px;'>Heat Level: {fire_state['heat']}</div>", unsafe_allow_html=True)

st.subheader("🌫️ Smoke Sensor")
st.markdown(f"<div style='background-color:{get_color(fire_state['smoke'])}; padding:8px; border-radius:6px;'>Smoke Level: {fire_state['smoke']}</div>", unsafe_allow_html=True)

st.subheader("🧪 Chemical Sensor")
st.markdown(f"<div style='background-color:{get_color(fire_state['chemicals'])}; padding:8px; border-radius:6px;'>Chemical Level: {fire_state['chemicals']}</div>", unsafe_allow_html=True)

# --- Reset Button ---
if st.button("🔄 Reset Sensors"):
    fire_state.update({
        "heat": 0,
        "smoke": 0,
        "chemicals": 0,
        "fire": False
    })

# --- Fire Alarm Auto-Trigger ---
if (fire_state["heat"] >= 80 or fire_state["smoke"] >= 70 or fire_state["chemicals"] >= 60):
    fire_state["fire"] = True

if fire_state["fire"]:
    st.error("🚨 FIRE ALARM TRIGGERED!")
else:
    st.success("✅ System Normal")

# --- Limit Sensor Max Values ---
for key in ["heat", "smoke", "chemicals"]:
    fire_state[key] = min(fire_state[key], 100)

# --- Save Updated State ---
with open(signal_file, "w") as f:
    json.dump(fire_state, f)

st.info("🔄 Press **R** or refresh browser to simulate next update!")
