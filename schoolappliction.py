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

# Make sure the image file is present
if not os.path.exists("basement.png1"):
    st.error("basement.png not found in this directory.")
    st.stop()

# Encode the image
with open("basement.png", "rb") as f:
    encoded_string = base64.b64encode(f.read()).decode()

# HTML code with escaped curly braces for JS objects
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
      border: none;
    }}
    #openseadragon, .openseadragon-container {{
      width: 100vw;
      height: 100vh;
      margin: 0;
      padding: 0;
      border: none;
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
  <div id="openseadragon"></div>
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

# Render the viewer
components.html(html_code, height=1501, scrolling=False)
