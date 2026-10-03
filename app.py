from __future__ import annotations

import base64
import json
import re
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
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
HASH_PATTERN = re.compile(r"^[a-f0-9]{64}$")


def _param(name: str, default: str = "") -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def _set_query(page: str) -> None:
    st.query_params.clear()
    st.query_params["page"] = page


def _init_session() -> None:
    st.session_state.setdefault("demo_users", {})
    st.session_state.setdefault("auth_user", None)
    st.session_state.setdefault("auth_feedback", None)


def _handle_auth_action() -> None:
    action = _param("auth_action").strip().lower()
    if not action:
        return

    users = st.session_state["demo_users"]
    email = _param("email").strip().lower()
    password_hash = _param("password_hash").strip().lower()
    name = _param("name").strip()

    feedback: dict[str, str] | None = None
    next_page = "home"

    if action == "register":
        if len(name) < 2:
            feedback = {
                "mode": "register",
                "title": "Registration failed",
                "message": "Please enter your full name.",
                "next": "login",
            }
        elif not EMAIL_PATTERN.fullmatch(email):
            feedback = {
                "mode": "register",
                "title": "Registration failed",
                "message": "Please enter a valid email address.",
                "next": "login",
            }
        elif not HASH_PATTERN.fullmatch(password_hash):
            feedback = {
                "mode": "register",
                "title": "Registration failed",
                "message": "Password was not submitted correctly. Please try again.",
                "next": "login",
            }
        elif email in users:
            feedback = {
                "mode": "login",
                "title": "Account already exists",
                "message": "This email is already registered. Please log in.",
                "next": "login",
            }
        else:
            users[email] = {"name": name, "password_hash": password_hash}
            st.session_state["auth_user"] = {"name": name, "email": email}
            next_page = "dashboard"

    elif action == "login":
        user = users.get(email)
        if not EMAIL_PATTERN.fullmatch(email) or not HASH_PATTERN.fullmatch(password_hash):
            feedback = {
                "mode": "login",
                "title": "Login failed",
                "message": "Please enter a valid email and password.",
                "next": "login",
            }
        elif not user or user.get("password_hash") != password_hash:
            feedback = {
                "mode": "login",
                "title": "Login failed",
                "message": "Invalid email or password.",
                "next": "login",
            }
        else:
            st.session_state["auth_user"] = {"name": user["name"], "email": email}
            next_page = "dashboard"

    elif action == "logout":
        st.session_state["auth_user"] = None
        next_page = "home"

    st.session_state["auth_feedback"] = feedback
    _set_query(next_page)
    st.rerun()


def _current_page() -> str:
    requested = _param("page", "home")
    if requested == "dashboard" and not st.session_state.get("auth_user"):
        return "home"
    return "dashboard" if requested == "dashboard" else "home"


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


def _inject_navigation_and_assets(
    html: str,
    page: str,
    avatar_url: str,
    auth_user: dict[str, str] | None,
    auth_feedback: dict[str, str] | None,
) -> str:
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
[data-testid="stAppViewContainer"] { overflow-x: hidden; }
@media (max-width: 640px) {
  .wrap { width: min(100%, calc(100% - 24px)) !important; }
}
</style>
"""

    dashboard_overrides = """
<style>
html, body { height: auto !important; min-height: 100% !important; }
body { overflow: auto !important; }
.app { gap: 14px !important; padding: 14px !important; min-height: calc(100vh - 64px); }
aside.left, aside.right, .recent { overflow: visible !important; }
.msgs { max-height: min(58vh, 680px); }
@media (max-width: 860px) {
  .top { padding: 0 12px !important; }
  .app { padding: 10px !important; }
  .msgs { max-height: none !important; padding: 14px !important; }
  .chips { justify-content: flex-start !important; padding: 0 12px 12px !important; }
  .input { margin: 0 12px 12px !important; }
}
</style>
"""
    if page == "dashboard":
        responsive_style += dashboard_overrides

    if "</head>" in html:
        html = html.replace("</head>", responsive_style + "</head>", 1)

    auth_json = json.dumps(auth_user or {})
    feedback_json = json.dumps(auth_feedback or {})

    nav_script = f"""
<script>
const __AURA_PAGE = {json.dumps(page)};
const __AURA_AUTH_USER = {auth_json};
const __AURA_AUTHENTICATED = Boolean(__AURA_AUTH_USER && __AURA_AUTH_USER.email);
const __AURA_FEEDBACK = {feedback_json};

function __auraNavigate(page, extras = {{}}) {{
  const target = new URL(window.parent.location.href);
  target.searchParams.set('page', page);
  ['auth_action', 'email', 'password_hash', 'name'].forEach((k) => target.searchParams.delete(k));
  Object.entries(extras || {{}}).forEach(([k, v]) => {{
    if (v === null || v === undefined || v === '') target.searchParams.delete(k);
    else target.searchParams.set(k, String(v));
  }});
  window.parent.location.href = target.toString();
}}

async function __auraHash(value) {{
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}}

async function __auraSubmitAuth(action, payload = {{}}) {{
  const target = new URL(window.parent.location.href);
  target.searchParams.set('page', 'home');
  target.searchParams.set('auth_action', action);
  Object.entries(payload).forEach(([k, v]) => target.searchParams.set(k, String(v)));
  window.parent.location.href = target.toString();
}}

const __auraSetFrameHeight = () => {{
  const bodyHeight = document.body ? document.body.scrollHeight : 0;
  const docHeight = document.documentElement ? document.documentElement.scrollHeight : 0;
  const height = Math.max(bodyHeight, docHeight);
  window.parent.postMessage(
    {{
      isStreamlitMessage: true,
      type: "streamlit:setFrameHeight",
      height
    }},
    "*"
  );
}};

window.addEventListener("load", __auraSetFrameHeight);
window.addEventListener("resize", __auraSetFrameHeight);
if ("ResizeObserver" in window && document.body) {{
  new ResizeObserver(__auraSetFrameHeight).observe(document.body);
}}

if (__AURA_PAGE === 'home') {{
  const loginForm = document.getElementById('paneLogin');
  const registerForm = document.getElementById('paneRegister');
  const noticeButton = document.getElementById('nBtn');

  if (loginForm && typeof validate === 'function') {{
    loginForm.addEventListener('submit', async (event) => {{
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!validate(loginForm, 'login')) return;
      const email = loginForm.elements.email.value.trim().toLowerCase();
      const passwordHash = await __auraHash(loginForm.elements.password.value);
      __auraSubmitAuth('login', {{ email, password_hash: passwordHash }});
    }}, true);
  }}

  if (registerForm && typeof validate === 'function') {{
    registerForm.addEventListener('submit', async (event) => {{
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!validate(registerForm, 'register')) return;
      const name = registerForm.elements.name.value.trim();
      const email = registerForm.elements.email.value.trim().toLowerCase();
      const passwordHash = await __auraHash(registerForm.elements.password.value);
      __auraSubmitAuth('register', {{ name, email, password_hash: passwordHash }});
    }}, true);
  }}

  document.querySelectorAll('[data-route]').forEach((link) => {{
    link.addEventListener('click', (event) => {{
      event.preventDefault();
      event.stopImmediatePropagation();
      if (link.dataset.route === 'chat' && __AURA_AUTHENTICATED) {{
        __auraNavigate('dashboard');
        return;
      }}
      openModal(link.dataset.route === 'register' ? 'register' : 'login');
    }}, true);
  }});

  if (noticeButton) {{
    noticeButton.addEventListener('click', (event) => {{
      event.preventDefault();
      event.stopImmediatePropagation();
      if (noticeButton.dataset.next === 'login') {{
        noticeButton.dataset.next = '';
        openModal('login');
      }} else {{
        __auraNavigate('dashboard');
      }}
    }}, true);
  }}

  if (__AURA_FEEDBACK && __AURA_FEEDBACK.message) {{
    openModal(__AURA_FEEDBACK.mode || 'login');
    showNotice(__AURA_FEEDBACK.title || 'Authentication update', __AURA_FEEDBACK.message, (__AURA_FEEDBACK.next === 'login') ? 'Back to login' : 'Enter Aura');
    if (noticeButton) noticeButton.dataset.next = __AURA_FEEDBACK.next || 'login';
  }}
}}

if (__AURA_PAGE === 'dashboard') {{
  const fullName = (__AURA_AUTH_USER.name || '').trim() || 'Aura User';
  const firstName = fullName.split(/\\s+/)[0] || 'Friend';
  const uname = document.getElementById('uname');
  if (uname) uname.textContent = fullName;
  document.querySelectorAll('.un').forEach((el) => (el.textContent = firstName));

  const userChip = document.querySelector('.user');
  if (userChip && __AURA_AUTH_USER.email) userChip.title = __AURA_AUTH_USER.email;

  const tools = document.querySelector('.tools');
  if (tools && !document.getElementById('logoutBtn')) {{
    const logoutButton = document.createElement('button');
    logoutButton.id = 'logoutBtn';
    logoutButton.type = 'button';
    logoutButton.className = 'btn';
    logoutButton.textContent = 'Logout';
    logoutButton.style.padding = '8px 14px';
    logoutButton.style.borderRadius = '10px';
    logoutButton.style.border = '1px solid rgba(77,140,255,.35)';
    logoutButton.style.background = 'rgba(31,139,255,.12)';
    logoutButton.style.cursor = 'pointer';
    logoutButton.addEventListener('click', () => __auraSubmitAuth('logout'));
    tools.appendChild(logoutButton);
  }}
}}
</script>
"""
    return html.replace("</body>", nav_script + "</body>", 1)


def _inject_streamlit_layout_css() -> None:
    st.markdown(
        """
<style>
[data-testid="stAppViewContainer"] .main .block-container {
  max-width: 100%;
  padding: 0;
}
</style>
""",
        unsafe_allow_html=True,
    )


_init_session()
_handle_auth_action()

page = _current_page()
html_path = DASHBOARD_FILE if page == "dashboard" else INDEX_FILE
html_source = _read_text(html_path, html_path.name)
avatar_url = _avatar_data_url()

if page == "home":
    st.caption("Session-based demo authentication. Accounts reset when the app session ends.")

if html_source and avatar_url:
    _inject_streamlit_layout_css()
    rendered_html = _inject_navigation_and_assets(
        html_source,
        page,
        avatar_url,
        st.session_state.get("auth_user"),
        st.session_state.get("auth_feedback"),
    )
    st.session_state["auth_feedback"] = None
    components.html(rendered_html, height=900 if page == "dashboard" else 1200, scrolling=False)
