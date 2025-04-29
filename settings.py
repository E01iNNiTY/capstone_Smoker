import streamlit as st

# 1) Check for settings flag *before* any HTML injection
params = st.experimental_get_query_params()
if "settings" in params:
    st.title("⚙️ Settings")
    # ... your sliders, buttons, etc. ...
    st.stop()   # don’t run the rest of the script

# 2) If we get here, settings wasn’t in the URL: render the map
st.write("🌎 This is your map page")
# ... all your existing map HTML/JS ...
