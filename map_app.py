import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import json

st.set_page_config(layout="wide", page_title="Smart Fire Map")

# Read alarm signal state from shared file
fire_signal_file = "fire_signal.json"
if os.path.exists(fire_signal_file):
    with open(fire_signal_file, "r") as f:
        fire_data = json.load(f)
        show_alarm = fire_data.get("fire", False)
else:
    show_alarm = False

# Hide Streamlit UI & default padding
hide_streamlit_style = """
<style>
  header, footer, #MainMenu {
    visibility: hidden;
  }
  .block-container, .main, [data-testid="stAppViewContainer"] {
    margin: 0;
    padding: 0;
  }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Ensure image exists
if not os.path.exists("basement.png"):
    st.error("basement.png not found in this directory.")
    st.stop()

# Encode image to base64
with open("basement.png", "rb") as f:
    encoded_string = base64.b64encode(f.read()).decode()

# JavaScript for fire alert bubble
fire_alert_js = f"""
const fireBubble = document.getElementById("fire-alert");
if (fireBubble) {{
  fireBubble.style.display = {"'block'" if show_alarm else "'none'"};
}}
"""

# JavaScript for alarm icon on map
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
      new OpenSeadragon.Point(0.42, 0.31),
      OpenSeadragon.Placement.CENTER
    );
    """

# Final HTML layout
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://openseadragon.github.io/openseadragon/openseadragon.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
    }}
    html, body {{
      width: 100vw;
      height: 100vh;
      background: #f5f7fa;
      overflow: hidden;
    }}
    #openseadragon {{
      width: 100vw;
      height: 100vh;
      background-color: #f5f7fa;
    }}
    .top-bar {{
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 9999;
      display: flex;
      align-items: center;
      gap: 10px;
      background: white;
      padding: 12px 24px;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .top-bar input {{
      padding: 10px 18px;
      width: 280px;
      border-radius: 10px;
      border: 1px solid #ccc;
      font-size: 15px;
    }}
    .left-nav {{
      position: fixed;
      top: 100px;
      left: 20px;
      z-index: 9999;
      background: white;
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      font-size: 16px;
      line-height: 1.6;
    }}
    .top-right {{
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      background: rgba(255,255,255,0.85);
      padding: 10px 16px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      gap: 14px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
      backdrop-filter: blur(6px);
    }}
    .bottom-right {{
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      background: white;
      border: 2px solid #e53935;
      border-radius: 50%;
      width: 48px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      color: #e53935;
      box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }}
    @keyframes pulse {{
      0% {{ transform: scale(1); }}
      50% {{ transform: scale(1.15); }}
      100% {{ transform: scale(1); }}
    }}
  </style>
</head>
<body>
  <div id="openseadragon"></div>
  <div class="top-bar">
    <input type="text" placeholder="Search floors...">
  </div>
  <div class="left-nav">
    <div><strong>☰ Navigation</strong></div>
    <div>🧭 Map Controls</div>
    <div>📍 Zones</div>
  </div>
  <div class="top-right">
    <div style="position: relative;">
      🔥🔥🔥
      <div id="fire-alert" style="display: none; position: absolute; top: -15px; right: -5px;
           background: #e53935; color: white; padding: 4px 10px; border-radius: 14px;
           font-size: 13px; font-weight: 600; animation: pulse 1s infinite;">
        FIRE!
      </div>
    </div>
    <img src="https://via.placeholder.com/32" alt="User" style="
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 2px solid #ccc;
    ">
  </div>
  <div class="bottom-right">ⓘ</div>
  <script>
    const viewer = OpenSeadragon({
      id: "openseadragon",
      prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
      tileSources: {
        type: "image",
        url: "data:image/png;base64,{encoded_string}"
      },
      background: "#f5f7fa",
      letterboxColor: "#f5f7fa",
      homeFillsViewer: true,
      showNavigator: true,
      showNavigationControl: true,
      visibilityRatio: 1.0,
      minZoomLevel: 0.2,
      maxZoomLevel: 25
    });

    // ✅ Use OpenSeadragon API to disable controls after viewer opens
    viewer.addOnceHandler('open', function () {
      viewer.setControlsEnabled(false);
    });

    {alarm_script}
    {fire_alert_js}
  </script>
</body>
</html>
"""

components.html(html_code, height=1501, scrolling=False)

