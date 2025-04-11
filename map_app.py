import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import json
from auth import login

st.set_page_config(layout="wide", page_title="Smart Fire Map")

# 🔐 Authenticate first
if not login():
    st.stop()

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], .block-container {
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh !important;
        overflow: hidden !important;
        background-color: #f1ede4;
    }

    iframe {
        display: block;
        border: none;
    }

    header, footer, #MainMenu {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# 🔥 Read fire signal state
fire_signal_file = "fire_signal.json"
if os.path.exists(fire_signal_file):
    with open(fire_signal_file, "r") as f:
        fire_data = json.load(f)
        show_alarm = fire_data.get("fire", False)
else:
    show_alarm = False

# 🗺️ Load map
if not os.path.exists("basement.png"):
    st.error("Map image (basement.png) not found.")
    st.stop()

with open("basement.png", "rb") as f:
    map_base64 = base64.b64encode(f.read()).decode()

# 🏫 Load school logo
if not os.path.exists("mptv.png"):
    st.error("Logo image (mptv.png) not found.")
    st.stop()

with open("mptv.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

#  Fire alert bubble logic
fire_alert_js = f"""
const fireBubble = document.getElementById("fire-alert");
if (fireBubble) {{
  fireBubble.style.display = {"'block'" if show_alarm else "'none'"};
}}
"""

# Fire map overlay logic
alarm_script = ""
if show_alarm:
    alarm_script = """
    const alarm = document.createElement("div");
    alarm.innerHTML = "🚨";
    alarm.style.fontSize = "32px";
    alarm.style.animation = "blinker 1s linear infinite";
    alarm.style.pointerEvents = "none";

    const style = document.createElement("style");
    style.innerHTML = `
      @keyframes blinker {{
        50% {{ opacity: 0; }}
      }}
    `;
    document.head.appendChild(style);

    viewer.addOverlay(
      alarm,
      new OpenSeadragon.Point(0.47, 0.30),
      OpenSeadragon.Placement.CENTER
    );
    """


html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://openseadragon.github.io/openseadragon/openseadragon.min.js"></script>
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      background: #F0E8DA;
      font-family: sans-serif;
    }}

    #openseadragon,
    .openseadragon-container {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100vw !important;
      height: 100vh !important;
      background-color: #f1ede4;
    }}

    .top-bar {{
      position: fixed;
      top: 15px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
    }}

    .top-bar input {{
      padding: 8px 20px;
      width: 250px;
      border-radius: 16px;
      border: 1px solid #ccc;
      font-size: 14px;
    }}

    .top-right {{
      position: fixed;
      top: 15px;
      right: 20px;
      z-index: 1000;
      display: flex;
      align-items: flex-start;
      gap: 14px;
    }}

    .top-right img {{
      width: 32px;
      height: 32px;
      border-radius: 50%;
      border: 1px solid #888;
    }}

    #fire-alert {{
      display: none;
      background: red;
      color: white;
      padding: 2px 8px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: bold;
      position: absolute;
      top: -8px;
      right: -5px;
      animation: pulse 1s infinite;
    }}

    @keyframes pulse {{
      0% {{ transform: scale(1); }}
      50% {{ transform: scale(1.2); }}
      100% {{ transform: scale(1); }}
    }}
  </style>
</head>
<body>

  <div id="openseadragon"></div>

  <!-- Search -->
  <div class="top-bar">
    <input type="text" placeholder="Search Floors...">
  </div>

  <!-- Fire alert, sensor bar, and logo -->
  <div class="top-right">
    <!-- Fire Alert Column -->
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <!-- Fire Emojis -->
      <div style="position: relative;">
        🔥🔥🔥
        <div id="fire-alert">FIRE!</div>
      </div>

      <!-- Sensor Bars -->
      <div id="sensor-status" style="
        margin-top: 6px;
        display: flex;
        flex-direction: column;
        gap: 4px;
        font-size: 13px;
        font-weight: 500;
      ">
        <div id="heat-status" style="background: #fff; padding: 2px 10px; border-radius: 12px;">🌡️ Heat: Normal</div>
        <div id="smoke-status" style="background: #fff; padding: 2px 10px; border-radius: 12px;">🌫️ Smoke: Clear</div>
        <div id="chem-status" style="background: #fff; padding: 2px 10px; border-radius: 12px;">🧪 Chemicals: Safe</div>
      </div>
    </div>

  
<img src="data:image/png;base64,{logo_base64}" alt="Logo" style="
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid #888;
  margin-top: 2px;
">

  </div>

  <script>
    const viewer = OpenSeadragon({{
      id: "openseadragon",
      prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
      tileSources: {{
        type: "image",
        url: "data:image/png;base64,{map_base64}"
      }},
      background: "##F0E8DA",
      letterboxColor: "##F0E8DA",
      homeFillsViewer: true,
      showNavigator: false,
      showNavigationControl: true,
      visibilityRatio: 1.0,
      minZoomLevel: 0.2,
      maxZoomLevel: 25
    }});

    {alarm_script}
    {fire_alert_js}

    if ({'true' if show_alarm else 'false'}) {{
      document.getElementById("heat-status").style.background = "#e53935";
      document.getElementById("heat-status").innerText = "🌡️ Heat: HIGH";

      document.getElementById("smoke-status").style.background = "#e53935";
      document.getElementById("smoke-status").innerText = "🌫️ Smoke: Detected";

      document.getElementById("chem-status").style.background = "#e53935";
      document.getElementById("chem-status").innerText = "🧪 Chemicals: Unsafe";
    }}
  </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=False)
