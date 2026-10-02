from __future__ import annotations

import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

from agent import run_aura
from firebase_service import (
    firebase_available,
    login_user,
    register_user,
    send_login_notification,
)
from memory import ConversationMemory
from rag import retrieve_context
from security import sanitize_output, validate_user_input

# -----------------------------------------------------------------------------
# Configuration & Asset Paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

def _first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]

AVATAR = _first_existing(
    ASSETS_DIR / "aura_avatar.jpg",
    BASE_DIR / "aura_avatar.jpg",
)

st.set_page_config(
    page_title="AuraAI — AI Career & Skills Navigator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit default UI chrome
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #030a1f; color: #f2f6ff; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    iframe { width: 100% !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Complete Interactive Frontend Prototype (HTML/CSS/JS)
# -----------------------------------------------------------------------------
aura_app_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AuraAI | AI Career &amp; Skills Navigator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root{{
  --bg-0:#030a1f; --bg-1:#061a45; --bg-2:#0a2a6b;
  --panel:rgba(12,34,84,.55); --panel-solid:#0b2253;
  --line:rgba(77,140,255,.28);
  --blue:#1f8bff; --blue-d:#1468d6; --cyan:#22e0c0; --violet:#b07cff;
  --text:#f2f6ff; --muted:#9db4dd;
  --font:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font);color:var(--text);background:var(--bg-0);line-height:1.6;min-height:100vh;display:flex;flex-direction:column}}
body::before{{content:"";position:fixed;inset:0;z-index:-1;
  background:
   radial-gradient(900px 500px at 85% 12%,rgba(31,139,255,.28),transparent 60%),
   radial-gradient(700px 500px at 5% 0%,rgba(20,104,214,.25),transparent 60%),
   linear-gradient(160deg,var(--bg-0) 0%,var(--bg-1) 55%,#08235a 100%)}}
a{{color:inherit;text-decoration:none}}
.wrap{{width:min(1180px,92%);margin-inline:auto}}

/* Header */
header{{position:sticky;top:0;z-index:20;background:rgba(3,10,31,.72);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}}
.bar{{display:flex;align-items:center;justify-content:space-between;height:72px;padding:0 24px}}
.brand{{display:flex;align-items:center;gap:12px;cursor:pointer}}
.brand svg{{width:34px;height:34px;filter:drop-shadow(0 0 10px rgba(31,139,255,.8)}}
.brand b{{font-size:1.65rem;font-weight:800;letter-spacing:-.02em}}
.brand b span{{color:var(--blue)}}
.brand i{{font-style:normal;color:var(--muted);font-size:.92rem;padding-left:14px;border-left:1px solid var(--line)}}
nav{{display:flex;align-items:center;gap:6px}}
nav a.link{{padding:10px 20px;border-radius:12px;font-weight:600;font-size:.95rem;color:#d6e3ff;transition:background .2s,color .2s;cursor:pointer}}
nav a.link:hover{{background:rgba(31,139,255,.16)}}
nav a.link.active{{background:linear-gradient(180deg,#1f8bff,#1468d6);color:#fff;box-shadow:0 6px 20px rgba(31,139,255,.35)}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:10px 22px;border-radius:12px;font:600 .95rem var(--font);cursor:pointer;border:1px solid var(--line);color:var(--text);background:transparent;transition:all .2s}}
.btn:hover{{background:rgba(31,139,255,.14)}}
.btn.primary{{background:linear-gradient(180deg,#2b97ff,#1468d6);border-color:transparent;box-shadow:0 8px 24px rgba(31,139,255,.4)}}
.btn.primary:hover{{box-shadow:0 10px 30px rgba(31,139,255,.6)}}
.btn.lg{{padding:15px 30px;font-size:1.02rem}}
.nav-actions{{display:flex;gap:10px;margin-left:10px}}

/* Views Container */
.view-container {{ display: none; flex: 1; }}
.view-container.active {{ display: block; }}

/* Hero */
.hero{{display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center;padding:70px 0 40px}}
.badge{{display:inline-flex;align-items:center;gap:8px;padding:8px 18px;border:1px solid var(--line);border-radius:999px;color:#7db8ff;font-weight:600;font-size:.9rem;background:rgba(31,139,255,.08)}}
h1{{font-size:clamp(2.6rem,6vw,4.6rem);line-height:1.04;font-weight:800;letter-spacing:-.035em;margin:26px 0 22px}}
h1 em{{font-style:normal;background:linear-gradient(90deg,#3aa0ff,#b07cff);-webkit-background-clip:text;background-clip:text;color:transparent}}
.lead{{color:var(--muted);font-size:1.12rem;max-width:560px;margin-bottom:34px}}
.portrait{{position:relative;justify-self:center;width:min(400px,80vw);aspect-ratio:1}}
.portrait::before{{content:"";position:absolute;inset:-18px;border-radius:50%;border:2px solid rgba(31,139,255,.65);box-shadow:0 0 50px rgba(31,139,255,.35),inset 0 0 40px rgba(31,139,255,.15)}}
.portrait img{{width:100%;height:100%;object-fit:cover;object-position:50% 20%;border-radius:50%;border:3px solid rgba(80,160,255,.8);display:block}}
.hello{{position:absolute;right:-30px;bottom:-40px;background:var(--panel-solid);border:1px solid var(--line);border-radius:18px;padding:16px 22px;box-shadow:0 18px 40px rgba(0,0,0,.45),0 0 30px rgba(31,139,255,.2)}}
.hello strong{{display:flex;align-items:center;gap:8px;font-size:1.08rem}}
.hello span{{color:var(--muted);font-size:.92rem}}

/* Features */
.features{{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;padding:30px 0 80px}}
.feat{{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:22px}}
.ico{{width:52px;height:52px;border-radius:14px;display:grid;place-items:center;margin-bottom:16px;background:linear-gradient(145deg,#12388a,#0b2253);border:1px solid var(--line);color:#4aa8ff}}
.feat h3{{font-size:1.05rem;margin-bottom:6px}}
.feat p{{color:var(--muted);font-size:.92rem}}

/* Dashboard UI Reference Replica */
.dash-app{{display:grid;grid-template-columns:278px 1fr 350px;gap:18px;padding:18px;height:calc(100vh - 72px);overflow:hidden}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:20px;min-height:0}}
aside.left{{display:flex;flex-direction:column;gap:16px;overflow:auto;padding:12px}}
.menu{{display:grid;gap:4px}}
.menu button{{display:flex;align-items:center;gap:14px;padding:13px 16px;border:0;border-radius:12px;background:none;color:#d6e3ff;font-size:.98rem;font-weight:500;cursor:pointer;text-align:left;transition:background .2s}}
.menu button:hover{{background:rgba(31,139,255,.14)}}
.menu button.on{{background:linear-gradient(180deg,#1f8bff,#1468d6);color:#fff;font-weight:600;box-shadow:0 6px 18px rgba(31,139,255,.35)}}
.card{{padding:18px}}
.card h4{{font-size:.95rem;font-weight:600;margin-bottom:12px}}
.prog{{display:flex;align-items:center;gap:14px}}
.ring{{width:70px;height:70px;border-radius:50%;flex:none;background:conic-gradient(var(--blue) 68%,rgba(255,255,255,.1) 0);display:grid;place-items:center}}
.ring span{{width:54px;height:54px;border-radius:50%;background:#0a2054;display:grid;place-items:center;font-weight:700;font-size:.95rem}}
.recent{{padding:16px;flex:1;overflow:auto}}
.chat-item{{display:flex;gap:12px;align-items:center;width:100%;padding:10px 6px;border:0;border-bottom:1px solid rgba(77,140,255,.15);background:none;text-align:left;cursor:pointer;border-radius:10px;color:inherit}}
.chat-item:hover{{background:rgba(31,139,255,.1)}}
.chat-item .ci{{width:34px;height:34px;border-radius:10px;background:rgba(31,139,255,.2);display:grid;place-items:center;color:#7db8ff;flex:none}}
.chat-item b{{display:block;font-size:.84rem;font-weight:500}}
.chat-item small{{color:var(--muted);font-size:.74rem}}

main.chat-main{{display:flex;flex-direction:column;overflow:hidden;background:var(--panel)}}
.c-head{{display:flex;justify-content:space-between;align-items:center;padding:16px 22px;border-bottom:1px solid var(--line)}}
.c-head div{{display:flex;align-items:center;gap:12px}}
.online{{display:flex;align-items:center;gap:8px;padding:7px 16px;border:1px solid rgba(34,224,192,.5);border-radius:999px;color:#7df0d8;font-size:.84rem;background:rgba(34,224,192,.06)}}
.online i{{width:9px;height:9px;border-radius:50%;background:var(--cyan);box-shadow:0 0 10px var(--cyan)}}
.msgs{{flex:1;overflow:auto;padding:22px;display:flex;flex-direction:column;gap:18px}}
.m{{display:flex;gap:12px;max-width:86%}}
.m.me{{align-self:flex-end;flex-direction:row-reverse}}
.m img,.m .av{{width:44px;height:44px;border-radius:50%;object-fit:cover;object-position:50% 20%;border:2px solid rgba(80,160,255,.7);flex:none}}
.bub{{padding:14px 18px;border-radius:18px;background:rgba(20,52,120,.7);border:1px solid var(--line);font-size:.94rem;line-height:1.6}}
.m.me .bub{{background:linear-gradient(180deg,#1b4a9a,#143b80);border-top-right-radius:6px}}
.bub time{{display:block;text-align:right;color:var(--muted);font-size:.72rem;margin-top:6px}}
.sec{{background:rgba(7,22,60,.65);border:1px solid var(--line);border-radius:14px;padding:16px;margin:12px 0}}
.sec section{{display:flex;gap:12px;padding:12px 0;border-bottom:1px solid rgba(77,140,255,.18)}}
.sec section:last-child{{border:0;padding-bottom:0}}
.sec .ic{{width:38px;height:38px;border-radius:10px;display:grid;place-items:center;color:#fff}}
.sec h5{{color:#4db3ff;font-size:.92rem;margin-bottom:4px}}
.sec ul{{padding-left:18px;font-size:.84rem;color:#dbe7ff;line-height:1.75}}
.chips{{display:flex;gap:10px;flex-wrap:wrap;padding:0 22px 12px}}
.chip{{padding:8px 16px;border-radius:999px;border:1px solid var(--line);background:rgba(31,139,255,.1);font-size:.8rem;cursor:pointer;color:#d6e3ff}}
.chip:hover{{background:rgba(31,139,255,.25)}}
.input-area{{display:flex;align-items:center;gap:10px;margin:0 22px 22px;padding:8px 8px 8px 16px;border:1px solid var(--line);border-radius:16px;background:rgba(3,10,31,.55)}}
.input-area input{{flex:1;background:none;border:0;color:var(--text);font:400 .95rem var(--font);outline:none}}
.send{{width:46px;height:40px;border:0;border-radius:12px;background:linear-gradient(180deg,#2b97ff,#1468d6);cursor:pointer;display:grid;place-items:center;color:#fff}}

aside.right{{display:flex;flex-direction:column;gap:16px;overflow:auto;padding:12px}}
.aura-profile{{position:relative;padding:20px;text-align:center}}
.aura-profile img{{width:160px;height:160px;border-radius:50%;object-fit:cover;border:2px solid rgba(31,139,255,.7);margin-bottom:12px}}
.facts{{display:grid;gap:10px}}
.fact{{display:flex;gap:12px;align-items:center;padding:10px;background:rgba(31,139,255,.1);border-radius:12px;border:1px solid var(--line);font-size:.82rem}}
.qa button{{display:flex;align-items:center;gap:12px;width:100%;padding:10px;margin-bottom:8px;border:1px solid var(--line);border-radius:10px;background:rgba(31,139,255,.1);cursor:pointer;color:inherit;text-align:left;font-size:.84rem}}

/* Modal Popup */
.overlay{{position:fixed;inset:0;z-index:50;display:none;align-items:center;justify-content:center;padding:20px;background:rgba(2,6,20,.72);backdrop-filter:blur(8px)}}
.overlay.show{{display:flex}}
.modal{{position:relative;width:min(440px,100%);background:linear-gradient(170deg,#0d2a66,#071a45);border:1px solid var(--line);border-radius:22px;padding:30px 28px;box-shadow:0 30px 80px rgba(0,0,0,.6)}}
.x{{position:absolute;top:14px;right:14px;width:36px;height:36px;border-radius:10px;border:1px solid var(--line);background:transparent;color:var(--muted);cursor:pointer}}
.seg{{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:4px;border:1px solid var(--line);border-radius:14px;background:rgba(3,10,31,.5);margin-bottom:20px}}
.seg button{{padding:10px;border:0;border-radius:10px;background:transparent;color:var(--muted);font-weight:600;cursor:pointer}}
.seg button.on{{background:linear-gradient(180deg,#2b97ff,#1468d6);color:#fff}}
.pane{{display:none;gap:14px}}
.pane.on{{display:grid}}
.field label{{font-size:.9rem;font-weight:600;display:grid;gap:6px;margin-bottom:10px}}
.field input{{padding:12px;border-radius:10px;background:rgba(3,10,31,.6);border:1px solid var(--line);color:var(--text);width:100%}}

/* Footer */
footer{{margin-top:auto;border-top:1px solid var(--line);background:rgba(3,10,31,.7);padding:28px 0}}
.foot{{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:.9rem;padding:0 24px}}
</style>
</head>
<body>

<header>
  <div class="bar">
    <div class="brand" onclick="switchView('home')">
      <svg viewBox="0 0 24 24" fill="#3aa0ff"><path d="M12 1.5c.6 5.2 2.6 8.1 5.6 9.2 1.5.5 3.1.8 5 1.3-4.6 1-7.4 2.6-9 5.4-.7 1.2-1.2 3-1.6 5.6-.4-2.6-.9-4.4-1.6-5.6-1.6-2.8-4.4-4.4-9-5.4 1.9-.5 3.5-.8 5-1.3 3-1.1 5-4 5.6-9.2z"/></svg>
      <b>Aura<span>AI</span></b><i>AI Career &amp; Skills Navigator</i>
    </div>
    <nav id="nav">
      <a class="link active" onclick="switchView('home')">Home</a>
      <a class="link" onclick="switchView('about')">About</a>
      <a class="link" onclick="switchView('contact')">Contact</a>
      <div class="nav-actions">
        <button class="btn" onclick="openModal('login')">Login</button>
        <button class="btn primary" onclick="openModal('register')">Register</button>
      </div>
    </nav>
  </div>
</header>

<!-- HOME VIEW -->
<div id="view-home" class="view-container active">
  <div class="wrap">
    <div class="hero">
      <div>
        <span class="badge">&#10022; Your AI Career Coach</span>
        <h1>Navigate your next move with <em>clarity.</em></h1>
        <p class="lead">AI Career &amp; Skills Navigator helps you identify skill gaps, find free learning resources, and explore real-time job market trends, all in one place[cite: 8].</p>
        <button class="btn primary lg" onclick="enterDashboard()">&#128172; Enter Aura</button>
      </div>
      <div class="portrait">
        <img src="https://raw.githubusercontent.com/Tajdar-Khalil/aura-ai-navigator/main/assets/aura_avatar.jpg" alt="Aura">
        <div class="hello">
          <strong>Hi, I'm Aura!</strong>
          <span>Your AI Career &amp; Skills Navigator[cite: 2]</span>
        </div>
      </div>
    </div>
    <div class="features">
      <div class="feat"><div class="ico"><i class="fa-solid fa-bullseye"></i></div><h3>Find Skill Gaps</h3><p>Discover what skills to build next[cite: 8].</p></div>
      <div class="feat"><div class="ico"><i class="fa-solid fa-book-open"></i></div><h3>Learn for Free</h3><p>Get curated free resources &amp; courses.</p></div>
      <div class="feat"><div class="ico"><i class="fa-solid fa-chart-line"></i></div><h3>Market Trends</h3><p>Explore real-time job opportunities.</p></div>
      <div class="feat"><div class="ico"><i class="fa-solid fa-compass"></i></div><h3>Build Your Future</h3><p>Get personalized career guidance[cite: 8].</p></div>
    </div>
  </div>
</div>

<!-- DASHBOARD VIEW -->
<div id="view-dashboard" class="view-container">
  <div class="dash-app">
    <aside class="left panel">
      <div class="menu">
        <button class="on"><i class="fa-solid fa-comments"></i> Chat with Aura</button>
        <button><i class="fa-solid fa-route"></i> Career Roadmap</button>
        <button><i class="fa-solid fa-pie-chart"></i> Skills</button>
        <button><i class="fa-solid fa-briefcase"></i> Opportunities</button>
        <button><i class="fa-solid fa-book"></i> Resources</button>
      </div>
      <div class="card panel" style="margin-top:10px">
        <h4>Your Progress</h4>
        <div class="prog">
          <div class="ring"><span>68%</span></div>
          <p style="font-size:0.85rem">Career Growth Journey</p>
        </div>
      </div>
      <div class="recent panel" style="margin-top:10px">
        <h4 style="margin-bottom:8px">Recent Chats</h4>
        <button class="chat-item">
          <div class="ci"><i class="fa-solid fa-file-lines"></i></div>
          <div><b>Web Application Security Career Path</b><small>2 hours ago</small></div>
        </button>
      </div>
    </aside>

    <main class="chat-main panel">
      <div class="c-head">
        <div><i class="fa-solid fa-atom" style="color:var(--blue)"></i><span><b>Chat with Aura</b><br><small style="color:var(--muted)">Your AI Career Coach[cite: 2]</small></span></div>
        <span class="online"><i></i>Aura is online[cite: 2]</span>
      </div>
      <div class="msgs" id="msg-feed">
        <div class="m me">
          <div class="av" style="background:#2b97ff;display:grid;place-items:center;border-radius:50%;width:40px;height:40px">You</div>
          <div class="bub">What skills should I learn to become a Web Application Security Engineer?[cite: 2]<time>10:24 AM ✓✓</time></div>
        </div>
        <div class="m">
          <img src="https://raw.githubusercontent.com/Tajdar-Khalil/aura-ai-navigator/main/assets/aura_avatar.jpg" alt="Aura">
          <div class="bub">
            <p>Great question! Becoming a Web Application Security Engineer requires a mix of technical skills, hands-on practice, and continuous learning[cite: 2]. Here's a structured breakdown:</p>
            <div class="sec">
              <section>
                <span class="ic" style="background:#1f6fe0"><i class="fa-solid fa-shield"></i></span>
                <div><h5>1. Core Security Skills</h5><ul><li>Web application security fundamentals &amp; OWASP Top 10[cite: 2]</li><li>Secure coding practices (HTML, JS, Python, PHP)[cite: 2]</li></ul></div>
              </section>
            </div>
            <time>10:24 AM</time>
          </div>
        </div>
      </div>
      <div class="chips">
        <button class="chip" onclick="sendPrompt('Show me a 90-day roadmap')">Show me a 90-day roadmap</button>
        <button class="chip" onclick="sendPrompt('Free learning resources')">Free learning resources</button>
      </div>
      <div class="input-area">
        <input id="user-input" placeholder="Type your message to Aura..." onkeydown="if(event.key==='Enter')submitMsg()">
        <button class="send" onclick="submitMsg()"><i class="fa-solid fa-paper-plane"></i></button>
      </div>
    </main>

    <aside class="right panel">
      <div class="aura-profile">
        <img src="https://raw.githubusercontent.com/Tajdar-Khalil/aura-ai-navigator/main/assets/aura_avatar.jpg" alt="Aura">
        <h3 style="font-size:1.4rem">Aura <span style="background:var(--blue);padding:2px 6px;border-radius:6px;font-size:0.7rem">AI</span>[cite: 2]</h3>
        <p style="color:var(--muted);font-size:0.85rem">Your Career Coach &amp; Guide[cite: 2]</p>
      </div>
      <div class="facts">
        <div class="fact"><i class="fa-solid fa-microchip" style="color:var(--blue);font-size:1.2rem"></i><div><b>GPT-OSS-120B</b><small style="color:var(--muted);display:block">Advanced reasoning[cite: 1]</small></div></div>
        <div class="fact"><i class="fa-solid fa-database" style="color:var(--cyan);font-size:1.2rem"></i><div><b>FAISS RAG</b><small style="color:var(--muted);display:block">Curated knowledge[cite: 1]</small></div></div>
      </div>
    </aside>
  </div>
</div>

<!-- ABOUT VIEW -->
<div id="view-about" class="view-container">
  <div class="wrap" style="padding:60px 0">
    <h2 style="font-size:2.5rem;margin-bottom:20px">About AuraAI</h2>
    <p style="color:var(--muted);font-size:1.1rem;max-width:700px;line-height:1.7">
      Aura is an intelligent AI-agent-based career guidance application designed to help users explore career paths, identify skill gaps, and make informed decisions using CrewAI, Groq, and FAISS RAG[cite: 1, 8].
    </p>
  </div>
</div>

<!-- CONTACT VIEW -->
<div id="view-contact" class="view-container">
  <div class="wrap" style="padding:60px 0">
    <h2 style="font-size:2.5rem;margin-bottom:20px">Contact Developer</h2>
    <p style="color:var(--muted);font-size:1.1rem">Developer Email: <strong style="color:var(--text)">tajdarkhalil099@gmail.com</strong></p>
  </div>
</div>

<!-- LOGIN / REGISTER MODAL -->
<div class="overlay" id="overlay">
  <div class="modal">
    <button class="x" onclick="closeModal()">&times;</button>
    <div class="seg">
      <button id="tab-login" class="on" onclick="setAuthTab('login')">Login</button>
      <button id="tab-register" onclick="setAuthTab('register')">Register</button>
    </div>
    <div id="pane-login" class="pane on">
      <div class="field"><label>Email<input type="email" id="login-email" placeholder="you@example.com"></label></div>
      <div class="field"><label>Password<input type="password" id="login-pass" placeholder="••••••••"></label></div>
      <button class="btn primary lg" style="width:100%;justify-content:center;margin-top:10px" onclick="handleAuth('login')">Sign In</button>
    </div>
    <div id="pane-register" class="pane">
      <div class="field"><label>Full Name<input type="text" placeholder="Your Name"></label></div>
      <div class="field"><label>Email<input type="email" placeholder="you@example.com"></label></div>
      <div class="field"><label>Password<input type="password" placeholder="At least 8 characters"></label></div>
      <button class="btn primary lg" style="width:100%;justify-content:center;margin-top:10px" onclick="handleAuth('register')">Create Account</button>
    </div>
  </div>
</div>

<footer>
  <div class="foot">
    <span>&copy; 2026 AuraAI — AI Career &amp; Skills Navigator. All rights reserved.</span>
    <span>Designed &amp; Developed by Tajdar</span>
  </div>
</footer>

<script>
function switchView(viewId) {{
  document.querySelectorAll('.view-container').forEach(el => el.classList.remove('active'));
  document.getElementById('view-' + viewId).classList.add('active');
  window.scrollTo(0, 0);
}}

function enterDashboard() {{
  switchView('dashboard');
}}

function openModal(mode) {{
  document.getElementById('overlay').classList.add('show');
  setAuthTab(mode);
}}

function closeModal() {{
  document.getElementById('overlay').classList.remove('show');
}

function setAuthTab(mode) {{
  document.getElementById('pane-login').classList.toggle('on', mode === 'login');
  document.getElementById('pane-register').classList.toggle('on', mode === 'register');
  document.getElementById('tab-login').classList.toggle('on', mode === 'login');
  document.getElementById('tab-register').classList.toggle('on', mode === 'register');
}}

function handleAuth(type) {{
  closeModal();
  switchView('dashboard');
}}

function sendPrompt(text) {{
  const feed = document.getElementById('msg-feed');
  feed.innerHTML += `<div class="m me"><div class="av" style="background:#2b97ff;display:grid;place-items:center;border-radius:50%;width:40px;height:40px">You</div><div class="bub">${{text}}<time>Just now ✓✓</time></div></div>`;
  feed.scrollTop = feed.scrollHeight;
  
  setTimeout(() => {{
    feed.innerHTML += `<div class="m"><img src="https://raw.githubusercontent.com/Tajdar-Khalil/aura-ai-navigator/main/assets/aura_avatar.jpg"><div class="bub"><p>I am analyzing your request regarding "${{text}}". Let me build a customized plan for you.</p><time>Just now</time></div></div>`;
    feed.scrollTop = feed.scrollHeight;
  }}, 800);
}}

function submitMsg() {{
  const input = document.getElementById('user-input');
  if(input.value.trim()) {{
    sendPrompt(input.value);
    input.value = '';
  }}
}}
</script>
</body>
</html>
"""

# Render full interactive prototype inside Streamlit
components.html(aura_app_html, height=920, scrolling=True)
