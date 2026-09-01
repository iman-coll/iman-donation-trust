"""
Iman Donation Trust — Streamlit shell
Renders the REAL web app (GitHub Pages) 1:1 inside a frameless embed.
Result: 100% identical to the GitHub Pages version, because it IS that app.
"""
import streamlit as st
import streamlit.components.v1 as components

# ✏️ EDIT if you ever rename the repo/username:
APP_URL = "https://iman-coll.github.io/iman-donation-trust/"
ORG = "Iman Donation Trust"

st.set_page_config(
    page_title=f"{ORG} — Donate with Love 💗",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Strip ALL Streamlit chrome so ONLY the embedded app is visible ──
CSS = """
<style>
  header[data-testid="stHeader"]{display:none;}
  #MainMenu{visibility:hidden;}
  footer{visibility:hidden;}
  [data-testid="stToolbar"]{display:none;}
  [data-testid="stDecoration"]{display:none;}
  [data-testid="stStatusWidget"]{display:none;}
  [data-testid="stSidebar"]{display:none;}
  section[data-testid="stSidebar"]{display:none;}
  .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
  [data-testid="stAppViewContainer"]{background:#ffe6ee;}
  /* Floating helper pill (top-right, never blocks the app) */
  #iman-pill{position:fixed;top:8px;right:12px;z-index:99999;
    background:#fff;border:2.5px solid #ffd9e6;border-radius:999px;
    padding:6px 12px;font:700 13px 'Baloo 2','Quicksand',sans-serif;color:#b0577c;
    box-shadow:0 6px 14px rgba(214,120,150,.2);}
  #iman-pill a{color:#e05a7a;text-decoration:none;font-weight:800;margin-right:10px;}
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Helper pill: fullscreen escape hatch + brand ──
st.markdown(
    f"""<div id="iman-pill">
      <a href="{APP_URL}" target="_blank" rel="noopener">⛶ Fullscreen</a>
      <span>💗 {ORG}</span>
    </div>""",
    unsafe_allow_html=True,
)

# ── Height tuner (only needed if your screen clips the app) ──
with st.expander("⚙️ Display settings"):
    height = st.slider("Embed height (px)", 600, 3200, 1400, 50)
    st.caption("Default 1400 is enough on most screens — the app scrolls inside the frame. "
               "If anything ever looks cut off, nudge this up.")

components.iframe(APP_URL, height=height, scrolling=True)

st.markdown(
    f"""<div style="text-align:center;color:#a08aa8;font:600 .8rem 'Quicksand',sans-serif;padding:6px 0 18px;">
      The app above is the live Iman Donation Trust web app ·
      <a href="{APP_URL}" target="_blank" rel="noopener" style="color:#e05a7a;">Open standalone ↗</a>
    </div>""",
    unsafe_allow_html=True,
)
