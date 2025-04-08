import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import json

st.set_page_config(layout="wide", page_title="Smart Fire Map")

# Hardcoded login credentials (for demo)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# Session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIN SCREEN ---
if not st.session_state.authenticated:
    st.markdown("<h3 style='text-align: center;'>🔒 Login Required</h3>", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    st.stop()  # Prevents the rest of the app from loading

# --- MAIN APP (AFTER LOGIN) ---
# Load fire alert flag
fire_signal_file = "fire_signal.json"
if os.path.exists(fire_signal_file):
    with open(fire_signal_file, "r") as f:
        fire_data = json.load(f)
        show_alarm = fire_data.get("fire", False)
else:
    show_alarm = False

# Hide Streamlit UI
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .block-container {padding: 0; margin: 0;}
    </style>
""", unsafe_allow_html=True)

# Load and encode the map image
if not os.path.exists("basement.png"):
    st.error("Map image (basement.png) not found.")
    st.stop()

with open("basement.png", "rb") as f:
    encoded_string = base64.b64encode(f.read()).decode()

# Fire alert logic
fire_alert_js = f"""
const fireBubble = document.getElementById("fire-alert");
if (fireBubble) {{
  fireBubble.style.display = {"'block'" if show_alarm else "'none'"};
}}
"""

# Fire icon on map
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
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      background: #f1ede4;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      font-family: sans-serif;
    }}
    #openseadragon {{
      width: 100vw;
      height: 100vh;
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
      align-items: center;
      gap: 10px;
    }}
    .top-right img {{
      width: 30px;
      height: 30px;
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

  <!-- Search bar -->
  <div class="top-bar">
    <input type="text" placeholder="Search Floors..">
  </div>

  <!-- Fire alert and icon -->
  <div class="top-right">
    <div style="position: relative;">
      🔥🔥🔥
      <div id="fire-alert">FIRE!</div>
    </div>
    <img src="https://via.placeholder.com/32" alt="User">
  </div>

  <script>
    const viewer = OpenSeadragon({{
      id: "openseadragon",
      prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
      tileSources: {{
        type: "image",
        url: "data:image/png;base64,{encoded_string}"
      }},
      background: "#f1ede4",
      letterboxColor: "#f1ede4",
      homeFillsViewer: true,
      showNavigator: false,
      showNavigationControl: true,
      visibilityRatio: 1.0,
      minZoomLevel: 0.2,
      maxZoomLevel: 25
    }});

    {alarm_script}
    {fire_alert_js}
  </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=False)
