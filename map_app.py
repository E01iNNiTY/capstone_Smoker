import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import json
from auth import login


import settings
st.write("MAMA HUEVO")
config = settings.load_settings()
default_zoom = config["default_zoom"]


st.set_page_config(layout="wide", page_title="Smart Fire Map")

if "logout" in st.query_params:
    with open("user_session.json", "w") as f:
        json.dump({"logged_in": False}, f)
    st.success("You’ve been logged out, Please Refresh To Log Back In.")
    st.stop()


if not login():
    st.stop()
# ⚙️ Sidebar settings UI
st.sidebar.header("Map Settings")
zoom_input = st.sidebar.number_input(
    "Default Zoom",
    min_value=0.1,
    max_value=10.0,
    step=0.1,
    value=default_zoom
)
if st.sidebar.button("Save Settings"):
    config["default_zoom"] = zoom_input
    settings.save_settings(config)
    st.sidebar.success(f"Saved default zoom = {zoom_input}")


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
      width: 100vw;
      height: 100vh;
      background-color: #F0E8DA;
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

 /* 📦 Collapsed side nav that slides open */
.side-nav {{
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 20px;  /* Super thin edge */
  background: rgba(33, 33, 33, 0.5);
  backdrop-filter: blur(6px);
  overflow: hidden;
  transition: width 0.3s ease, background 0.3s ease;
  z-index: 1100;
  border-right: 1px solid rgba(255,255,255,0.1);
  padding-top: 80px;
}}

.side-nav:hover {{
  width: 200px;
  background: rgba(33, 33, 33, 0.7);
}}

.nav-item {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  color: white;
  font-size: 16px;
  border-radius: 8px;
  transition: background 0.2s ease;
}}

.nav-item:hover {{
  background-color: rgba(255, 255, 255, 0.15);
}}

.nav-item .icon {{
  font-size: 20px;
}}

.nav-item .label {{
  opacity: 0;
  white-space: nowrap;
  transition: opacity 0.3s ease;
}}

.side-nav:hover .label {{
  opacity: 1;
}}


  </style>
</head>
<body>

<!-- Expandable Google Maps-style Side Nav -->
<div class="side-nav">
  <div class="nav-item">
    <span class="icon">⚙️</span>
    <span class="label">Settings</span>
  </div>
  <div class="nav-item">
    <span class="icon">🏢</span>
    <span class="label">Floors</span>
  </div>
 <div class="nav-item" id="logout-btn">
  <span class="icon">🚪</span>
  <span class="label">Logout</span>
</div>
  </div>

<!-- Map viewer -->
<div id="openseadragon"></div>

<!-- Search -->
<div class="top-bar" style="
  backdrop-filter: blur(3px);
  background-color: rgba(255, 255, 255, 0.05);
  padding: 6px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
">
  <input type="text" placeholder="Search Floors..." style="
    padding: 8px 16px;
    border-radius: 16px;
    border: 1px solid #ccc;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(2px);
    outline: none;
    font-size: 14px;
  ">
</div>





 <!-- Fire alert, sensor bar, and logo -->
<div class="top-right">

  <!-- Fire Alert Column (left side) -->
  <div style="display: flex; flex-direction: column; align-items: flex-start;">
    <!-- Fire Alert Emoji -->
    <div style="position: relative;">
      🔥🔥🔥🔥🔥🔥
      <div id="fire-alert">FIRE!</div>
    </div>

    <!-- Sensor Bars -->
    <div id="sensor-status" style="
      margin-top: 6px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 13px;
      font-weight: 500;
      color: white;
    ">

      <div id="heat-status" style="
        background-color: rgba(255, 255, 255, 0.1);
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px solid white;
        backdrop-filter: blur(6px);
      ">
        🌡️ Heat: Normal
      </div>

      <div id="smoke-status" style="
        background-color: rgba(255, 255, 255, 0.1);
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px solid white;
        backdrop-filter: blur(6px);
      ">
        🌫️ Smoke: Clear
      </div>

      <div id="chem-status" style="
        background-color: rgba(255, 255, 255, 0.1);
        padding: 6px 12px;
        border-radius: 6px;
        border: 1px solid white;
        backdrop-filter: blur(6px);
      ">
        🧪 Chemicals: Safe
      </div>
    </div>
  </div>

  <!-- Logo aligned to top right -->
  <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 1px solid #fff;
    background-color: rgba(255,255,255,0.1);
    padding: 2px;
    backdrop-filter: blur(6px);
  ">
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
      background: "#F0E8DA",
      letterboxColor: "##F0E8DA",
      homeFillsViewer: true,
      showNavigator: false,
      showNavigationControl: false,
      visibilityRatio: 1.0,
      minZoomLevel: 0.2,
      maxZoomLevel: 25
    }});

    {alarm_script}
    {fire_alert_js}

    document.getElementById("logout-btn").addEventListener("click", () => {{
      window.location.href = "?logout=true";
    }});

    
  </script>
</body>
</html>
"""


components.html(html_code, height=1500, scrolling=False)

