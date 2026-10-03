from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="AuraAI | AI Career & Skills Navigator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT_DIR = Path(__file__).resolve().parent
INDEX_FILE = ROOT_DIR / "index.html"
DASHBOARD_FILE = ROOT_DIR / "dashboard.html"
AVATAR_FILE = ROOT_DIR / "assets" / "aura_avatar.jpg"


def _current_page() -> str:
    page = st.query_params.get("page", "home")
    if isinstance(page, list):
        page = page[0] if page else "home"
    return "dashboard" if page == "dashboard" else "home"


def _read_text(path: Path, label: str) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        st.error(f"Missing required file: `{label}` ({path.name}).")
    except OSError as exc:
        st.error(f"Unable to read `{label}` ({path.name}): {exc}")
    return None


def _avatar_data_url() -> str | None:
    try:
        encoded = base64.b64encode(AVATAR_FILE.read_bytes()).decode("ascii")
    except FileNotFoundError:
        st.error("Missing required asset: `assets/aura_avatar.jpg`.")
        return None
    except OSError as exc:
        st.error(f"Unable to read `assets/aura_avatar.jpg`: {exc}")
        return None
    return f"data:image/jpeg;base64,{encoded}"


def _inject_navigation_and_assets(html: str, page: str, avatar_url: str) -> str:
    if page == "home":
        html = html.replace("window.location.href = 'dashboard.html';", "__auraNavigate('dashboard');")
    else:
        html = html.replace(
            'href="index.html"',
            'href="#" onclick="__auraNavigate(\'home\'); return false;"',
            1,
        )

    html = html.replace("aura_avatar.jpg", avatar_url)

    responsive_style = """
<style>
html, body { width: 100%; max-width: 100%; }
body { margin: 0; }
@media (max-width: 640px) {
  .wrap { width: min(100%, calc(100% - 24px)) !important; }
}
</style>
"""
    if "</head>" in html:
        html = html.replace("</head>", responsive_style + "</head>", 1)

    nav_script = """
<script>
function __auraNavigate(page) {
  const target = new URL(window.parent.location.href);
  target.searchParams.set('page', page);
  window.parent.location.href = target.toString();
}

const __auraSetFrameHeight = () => {
  const bodyHeight = document.body ? document.body.scrollHeight : 0;
  const docHeight = document.documentElement ? document.documentElement.scrollHeight : 0;
  const height = Math.max(bodyHeight, docHeight);
  window.parent.postMessage(
    {
      isStreamlitMessage: true,
      type: "streamlit:setFrameHeight",
      height
    },
    "*"
  );
};

window.addEventListener("load", __auraSetFrameHeight);
window.addEventListener("resize", __auraSetFrameHeight);
if ("ResizeObserver" in window && document.body) {
  new ResizeObserver(__auraSetFrameHeight).observe(document.body);
}
</script>
"""
    return html.replace("</body>", nav_script + "</body>", 1)


def _inject_streamlit_layout_css() -> None:
    st.markdown(
        """
<style>
[data-testid="stAppViewContainer"] .main .block-container {
  max-width: 100%;
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}

@media (max-width: 768px) {
  [data-testid="stAppViewContainer"] .main .block-container {
    padding-left: 0;
    padding-right: 0;
  }
}
</style>
""",
        unsafe_allow_html=True,
    )


page = _current_page()
html_path = DASHBOARD_FILE if page == "dashboard" else INDEX_FILE
html_source = _read_text(html_path, html_path.name)
avatar_url = _avatar_data_url()

if html_source and avatar_url:
    _inject_streamlit_layout_css()
    st.caption(
        "Demo notice: login/register flows in the embedded HTML are front-end-only placeholders "
        "and are not connected to real Firebase authentication in this deployment."
    )
    rendered_html = _inject_navigation_and_assets(html_source, page, avatar_url)
    components.html(rendered_html, height=1200 if page == "dashboard" else 1400, scrolling=False)
