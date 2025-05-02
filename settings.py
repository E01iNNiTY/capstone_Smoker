# settings.py
import json
import os

SETTINGS_FILE = "user_settings.json"
DEFAULTS = {
    "default_zoom": 1.0
}

def load_settings():
    """Load settings from disk, falling back to DEFAULTS."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}
    else:
        data = {}
    # merge with defaults
    return {**DEFAULTS, **data}

def save_settings(settings: dict):
    """Persist the given settings dict to disk."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)