import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(layout="wide")

# Hide Streamlit UI & remove default padding
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

# Check for image file
if not os.path.exists("basement.png"):
    st.error("basement.png not found in this directory.")
    st.stop()

# Encode image to base64
with open("basement.png", "rb") as f:
    encoded_string = base64.b64encode(f.read()).decode()

# HTML and embedded JS/CSS
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://openseadragon.github.io/openseadragon/openseadragon.min.js"></script>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    html, body {{
      width: 100vw;
      height: 100vh;
      background: #f0e8d9;
      overflow: hidden;
      overscroll-behavior: none;
      touch-action: none;
    }}
    #openseadragon, .openseadragon-container {{
      width: 100vw;
      height: 100vh;
      margin: 0;
      padding: 0;
      background-color: #f0e8d9;
    }}
    .openseadragon-container .openseadragon-button {{
      background-color: #f0e8d9;
      border-radius: 10px;
      box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
      transition: transform 0.2s ease;
    }}
    .openseadragon-container .openseadragon-button:hover {{
      transform: scale(1.1);
      background-color: #f0e8d9;
    }}
    .openseadragon-container .openseadragon-button img {{
      filter: brightness(200%) sepia(10%) contrast(120%);
    }}
  </style>
</head>
<body>

  <!-- Map Viewer -->
  <div id="openseadragon"></div>

  <!-- Top Search Bar -->
<div style="
  position: fixed;
  top: 20px;
  left: 150px;
  right: 150px;
  z-index: 9999;
  display: flex;
  justify-content: center;
  pointer-events: auto;
">
  <input type="text" placeholder="Search..." style="
    padding: 10px 20px;
    width: 300px;
    border-radius: 20px;
    border: 1px solid #ccc;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    font-size: 14px;
  ">
</div>

<!-- Left Nav Bar -->
<div style="
  position: fixed;
  top: 80px;
  left: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 15px;
  background: rgba(255,255,255,0.9);
  padding: 10px;
  border-radius: 8px;
  pointer-events: auto;
">
  <div><strong>☰ Nav</strong></div>
  <div>🧭 Map Control</div>
</div>

<!-- Top Right: Alerts and User Image -->
<div style="
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.9);
  padding: 6px 10px;
  border-radius: 20px;
  pointer-events: auto;
">
  <div>🔔🔔🔔</div>
  <img src="https://via.placeholder.com/32" alt="User" style="
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid #555;
  ">
</div>

<!-- Bottom Right Icon -->
<div style="
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  background: white;
  border: 2px solid #333;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  pointer-events: auto;
">
  ⓘ
</div>

  <!-- OpenSeadragon Script -->
  <script>
    var viewer = OpenSeadragon({{
      id: "openseadragon",
      prefixUrl: "https://openseadragon.github.io/openseadragon/images/",
      tileSources: {{
        type: "image",
        url: "data:image/png;base64,{encoded_string}"
      }},
      background: "#f0e8d9",
      letterboxColor: "#f0e8d9",
      homeFillsViewer: true,
      showNavigator: false,
      visibilityRatio: 1.0,
      minZoomLevel: 0.2,
      maxZoomLevel: 25
    }});
  </script>
</body>
</html>
"""

# Render full layout in Streamlit
components.html(html_code, height=1501, scrolling=False)
