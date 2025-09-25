from pathlib import Path
import json
import streamlit as st

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"

def load_css(st, path: str):
    css = Path(path).read_text(encoding="utf-8", errors="ignore")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def display_text(text):
    return st.markdown(f"""
    <div class="text-display">
        <p style="margin: 0;">{text}</p>
    </div>
    """,
    unsafe_allow_html=True
    )


def load_config():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

def update_config(key, value):
    data = load_config()
    data[key] = value
    CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")