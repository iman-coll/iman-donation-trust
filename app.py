# Iman Donation Trust — Streamlit shell (self-contained mirror)
# - Renders the repo's OWN index.html byte-for-byte (no external URL, no widgets)
# - Storage bridge: embed saves are mirrored to the Streamlit page's
#   localStorage so data survives Streamlit reruns and reloads.
# - JS iframe fitter: resizes the embed to the real viewport (no fragile CSS).
# - "Sync my data" box: paste a JSON export from any mirror to import it.
import json
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="Iman Donation Trust — Donate with Love 💗",
                   page_icon="💗", layout="wide", initial_sidebar_state="collapsed")

HIDE = """
<style>
  header[data-testid="stHeader"]{display:none;}
  #MainMenu{visibility:hidden;} footer{visibility:hidden;}
  [data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none;}
  [data-testid="stSidebar"],section[data-testid="stSidebar"]{display:none;}
  .block-container{padding:0 !important;margin:0 !important;max-width:100% !important;}
  [data-testid="stAppViewContainer"]{background:#ffe6ee;}
  #iman-pill{position:fixed;top:8px;right:12px;z-index:99999;background:#fff;
    border:2.5px solid #ffd9e6;border-radius:999px;padding:6px 12px;
    font:700 13px 'Baloo 2','Quicksand',sans-serif;color:#b0577c;
    box-shadow:0 6px 14px rgba(214,120,150,.2);}
  #iman-pill a{color:#e05a7a;text-decoration:none;font-weight:800;margin-right:10px;}
</style>"""
st.markdown(HIDE, unsafe_allow_html=True)

st.markdown(
    """<div id="iman-pill"><a href="./" target="_blank" rel="noopener">⛶ Reload</a>
    <span>💗 Iman Donation Trust</span></div>""",
    unsafe_allow_html=True,
)

BRIDGE = """
<script>
(function(){
  var MIRROR='imanMirrorV1';
  function load(){ try{ return JSON.parse(localStorage.getItem(MIRROR)||'{}'); }catch(e){ return {}; } }
  function save(o){ try{ localStorage.setItem(MIRROR, JSON.stringify(o)); }catch(e){} }
  window.addEventListener('message', function(e){
    var d=e.data||{};
    if(d.type==='imanNeedStore'){
      var fr=document.querySelectorAll('iframe');
      for(var i=0;i<fr.length;i++){
        try{ fr[i].contentWindow.postMessage({type:'imanStoreData', payload:JSON.stringify(load())}, '*'); }catch(err){}
      }
    } else if(d.type==='imanSave'){
      var o=load();
      if(d.value===null){ delete o[d.key]; } else { o[d.key]=String(d.value); }
      save(o);
    }
  });
  function fit(){
    var fr=document.querySelectorAll('iframe');
    for(var i=0;i<fr.length;i++){
      var f=fr[i];
      if(f.offsetWidth>300){ f.style.height=window.innerHeight+'px'; }
    }
  }
  window.addEventListener('load', fit);
  window.addEventListener('resize', fit);
  setInterval(fit, 800);
  fit();
})();
</script>"""
st.markdown(BRIDGE, unsafe_allow_html=True)

with st.expander("🔄 Sync my data (import a JSON export)"):
    st.caption("In this app or on GitHub Pages open Profile → ⬇️ Export my data, then paste the "
               "file's contents below and press Load. Your basket, history and profile are restored here.")
    raw = st.text_area("Paste exported JSON", height=140,
                       placeholder='{"profile":{...},"basket":[...],"history":[...]}')
    if st.button("📥 Load into app", type="primary"):
        try:
            d = json.loads(raw)
            if not isinstance(d, dict):
                raise ValueError
            st.session_state["_iman_import"] = json.dumps(d, ensure_ascii=False)
            st.success("Saved — the app is loading with your data…")
            st.rerun()
        except Exception:
            st.error("That did not look like valid Iman export JSON.")

BASE = Path(__file__).parent
html_path = BASE / "index.html"
if not html_path.exists():
    st.error("index.html was not found next to app.py — it must sit in the repo root.")
    st.stop()
HTML = html_path.read_text(encoding="utf-8")

# One-shot import injection (cleared after use so it never resurrects old data)
import_snip = ""
pending = st.session_state.pop("_iman_import", None)
if pending:
    safe = json.dumps(pending, ensure_ascii=False).replace("</", "<\\/")
    import_snip = "try{localStorage.setItem('iman-trust-v3', %s);}catch(e){}" % safe

SHIM = """<script>
(function(){
  if(window.__imanShim) return; window.__imanShim=1;
  function post(m){ try{ parent.postMessage(m,'*'); }catch(e){} }
  post({type:'imanNeedStore'});
  window.addEventListener('message', function(e){
    var d=e.data||{};
    if(d.type==='imanStoreData'){
      var inc={}; try{ inc=JSON.parse(d.payload||'{}'); }catch(err){ return; }
      var changed=false;
      for(var k in inc){
        try{ if(localStorage.getItem(k)!==inc[k]){ localStorage.setItem(k,inc[k]); changed=true; } }catch(e){}
      }
      var flag=0; try{ flag=+(sessionStorage.getItem('__imanR')||0); }catch(e){}
      if(changed && !flag){ try{ sessionStorage.setItem('__imanR','1'); }catch(e){} location.reload(); }
    }
  });
  try{
    var _s=localStorage.setItem.bind(localStorage), _r=localStorage.removeItem.bind(localStorage);
    localStorage.setItem=function(k,v){ _s(k,v); post({type:'imanSave',key:k,value:String(v)}); };
    localStorage.removeItem=function(k){ _r(k); post({type:'imanSave',key:k,value:null}); };
  }catch(e){}
})();
</script>
<script>%s</script>"""

SHIM_FULL = SHIM % import_snip
idx = HTML.find("<script>")
if idx == -1:
    st.error("index.html has no <script> tag — unexpected file.")
    st.stop()
HTML_OUT = HTML[:idx] + SHIM_FULL + HTML[idx:]

components.html(HTML_OUT, height=1000, scrolling=True)