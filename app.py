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

    nav_script = """
<script>
function __auraNavigate(page) {
  const target = new URL(window.parent.location.href);
  target.searchParams.set('page', page);
  window.parent.location.href = target.toString();
}
</script>
"""
    return html.replace("</body>", nav_script + "</body>", 1)


page = _current_page()
html_path = DASHBOARD_FILE if page == "dashboard" else INDEX_FILE
html_source = _read_text(html_path, html_path.name)
avatar_url = _avatar_data_url()

if html_source and avatar_url:
    st.caption(
        "Demo notice: login/register flows in the embedded HTML are front-end-only placeholders "
        "and are not connected to real Firebase authentication in this deployment."
    )
    rendered_html = _inject_navigation_and_assets(html_source, page, avatar_url)
    components.html(rendered_html, height=1300 if page == "dashboard" else 1800, scrolling=True)
