import streamlit as st
import streamlit.components.v1 as components
from agent import AuraAgent
from rag import RAGKnowledgeBase

st.set_page_config(
    page_title="AuraAI — AI Career & Skills Navigator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit Chrome & Apply Custom SaaS Dark Theme
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# Initialize Agent & RAG
agent = AuraAgent()
rag = RAGKnowledgeBase()

# HTML/CSS/JS Frontend Prototype matching the Exact Reference Dashboard
aura_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AuraAI | AI Career &amp; Skills Navigator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg-0:#030a1f; --bg-1:#061a45; --bg-2:#0a2a6b;
  --panel:rgba(12,34,84,.55); --panel-solid:#0b2253;
  --line:rgba(77,140,255,.28);
  --blue:#1f8bff; --blue-d:#1468d6; --cyan:#22e0c0; --violet:#b07cff;
  --text:#f2f6ff; --muted:#9db4dd;
  --font:'Plus Jakarta Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:84px}
body{font-family:var(--font);color:var(--text);background:var(--bg-0);line-height:1.6;min-height:100vh;display:flex;flex-direction:column}
body::before{content:"";position:fixed;inset:0;z-index:-1;
  background:
   radial-gradient(900px 500px at 85% 12%,rgba(31,139,255,.28),transparent 60%),
   radial-gradient(700px 500px at 5% 0%,rgba(20,104,214,.25),transparent 60%),
   linear-gradient(160deg,var(--bg-0) 0%,var(--bg-1) 55%,#08235a 100%)}
a{color:inherit;text-decoration:none}
:focus-visible{outline:2px solid var(--cyan);outline-offset:3px;border-radius:10px}
.wrap{width:min(1180px,92%);margin-inline:auto}

/* Header */
header{position:sticky;top:0;z-index:20;background:rgba(3,10,31,.72);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;height:72px;gap:16px}
.brand{display:flex;align-items:center;gap:12px}
.brand svg{width:34px;height:34px;filter:drop-shadow(0 0 10px rgba(31,139,255,.8))}
.brand b{font-size:1.65rem;font-weight:800;letter-spacing:-.02em}
.brand b span{color:var(--blue)}
.brand i{font-style:normal;color:var(--muted);font-size:.92rem;padding-left:14px;border-left:1px solid var(--line)}
nav{display:flex;align-items:center;gap:6px}
nav a.link{padding:10px 20px;border-radius:12px;font-weight:600;font-size:.95rem;color:#d6e3ff;transition:background .2s,color .2s}
nav a.link:hover{background:rgba(31,139,255,.16)}
nav a.link.active{background:linear-gradient(180deg,#1f8bff,#1468d6);color:#fff;box-shadow:0 6px 20px rgba(31,139,255,.35)}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 22px;border-radius:12px;font:600 .95rem var(--font);cursor:pointer;border:1px solid var(--line);color:var(--text);background:transparent;transition:transform .15s,box-shadow .2s,background .2s}
.btn:hover{background:rgba(31,139,255,.14)}
.btn:active{transform:translateY(1px)}
.btn.primary{background:linear-gradient(180deg,#2b97ff,#1468d6);border-color:transparent;box-shadow:0 8px 24px rgba(31,139,255,.4)}
.btn.primary:hover{box-shadow:0 10px 30px rgba(31,139,255,.6)}
.btn.lg{padding:15px 30px;font-size:1.02rem}
.nav-actions{display:flex;gap:10px;margin-left:10px}
.menu{display:none;background:none;border:1px solid var(--line);color:var(--text);border-radius:10px;width:42px;height:42px;font-size:1.3rem;cursor:pointer}

/* Hero */
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center;padding:70px 0 40px}
.badge{display:inline-flex;align-items:center;gap:8px;padding:8px 18px;border:1px solid var(--line);border-radius:999px;color:#7db8ff;font-weight:600;font-size:.9rem;background:rgba(31,139,255,.08)}
h1{font-size:clamp(2.6rem,6vw,4.6rem);line-height:1.04;font-weight:800;letter-spacing:-.035em;margin:26px 0 22px}
h1 em{font-style:normal;background:linear-gradient(90deg,#3aa0ff,#b07cff);-webkit-background-clip:text;background-clip:text;color:transparent}
.lead{color:var(--muted);font-size:1.12rem;max-width:560px;margin-bottom:34px}
.portrait{position:relative;justify-self:center;width:min(400px,80vw);aspect-ratio:1}
.portrait::before{content:"";position:absolute;inset:-18px;border-radius:50%;border:2px solid rgba(31,139,255,.65);box-shadow:0 0 50px rgba(31,139,255,.35),inset 0 0 40px rgba(31,139,255,.15)}
.portrait img{width:100%;height:100%;object-fit:cover;object-position:50% 20%;border-radius:50%;border:3px solid rgba(80,160,255,.8);display:block}
.hello{position:absolute;right:-30px;bottom:-40px;background:var(--panel-solid);border:1px solid var(--line);border-radius:18px;padding:16px 22px;box-shadow:0 18px 40px rgba(0,0,0,.45),0 0 30px rgba(31,139,255,.2)}
.hello strong{display:flex;align-items:center;gap:8px;font-size:1.08rem}
.hello strong svg{width:18px;height:18px}
.hello span{color:var(--muted);font-size:.92rem}
.dot{width:9px;height:9px;border-radius:50%;background:var(--cyan);box-shadow:0 0 10px var(--cyan)}

/* Features */
.features{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;padding:30px 0 80px}
.feat{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:22px;transition:border-color .2s,transform .2s}
.feat:hover{border-color:rgba(77,160,255,.6);transform:translateY(-3px)}
.ico{width:52px;height:52px;border-radius:14px;display:grid;place-items:center;margin-bottom:16px;background:linear-gradient(145deg,#12388a,#0b2253);border:1px solid var(--line);color:#4aa8ff}
.ico svg{width:24px;height:24px}
.feat h3{font-size:1.05rem;margin-bottom:6px}
.feat p{color:var(--muted);font-size:.92rem}

/* Sections */
section.block{padding:80px 0;border-top:1px solid var(--line)}
section.block h2{font-size:clamp(1.8rem,3.4vw,2.5rem);letter-spacing:-.025em;margin-bottom:14px}
.sub{color:var(--muted);max-width:640px;margin-bottom:34px}
.about-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:24px}
.card h3{margin-bottom:8px;font-size:1.05rem;color:#7db8ff}
.card p{color:var(--muted);font-size:.95rem}
.contact-grid{display:grid;grid-template-columns:1fr 1.1fr;gap:34px;align-items:start}
.info{display:grid;gap:14px}
.info div{display:flex;gap:14px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.info svg{width:22px;height:22px;color:#4aa8ff;flex:none}
form{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:26px;display:grid;gap:14px}
label{font-weight:600;font-size:.9rem;display:grid;gap:6px}
input,textarea{font:400 .95rem var(--font);color:var(--text);background:rgba(3,10,31,.6);border:1px solid var(--line);border-radius:12px;padding:12px 14px;width:100%}
input::placeholder,textarea::placeholder{color:#6f87b5}
input:focus,textarea:focus{outline:none;border-color:var(--blue);box-shadow:0 0 0 3px rgba(31,139,255,.25)}
textarea{min-height:120px;resize:vertical}
.ok{display:none;color:var(--cyan);font-weight:600}

/* Footer */
footer{margin-top:auto;border-top:1px solid var(--line);background:rgba(3,10,31,.7);padding:28px 0}
.foot{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px;color:var(--muted);font-size:.9rem}
.foot nav a{padding:6px 12px;color:var(--muted)}
.foot nav a:hover{color:var(--text)}

@media(max-width:960px){
  .hero{grid-template-columns:1fr;padding-top:44px}
  .portrait{margin:20px 0 50px}
  .hello{right:0}
  .features{grid-template-columns:repeat(2,1fr)}
  .about-grid,.contact-grid{grid-template-columns:1fr}
  .brand i{display:none}
  .menu{display:block}
  nav{position:absolute;top:72px;left:0;right:0;flex-direction:column;align-items:stretch;padding:14px 4%;background:rgba(3,10,31,.97);border-bottom:1px solid var(--line);display:none}
  nav.open{display:flex}
  .nav-actions{margin:8px 0 0}
  .nav-actions .btn{flex:1;justify-content:center}
}
@media(max-width:520px){.features{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
</style>
</head>
<body>

<header>
  <div class="wrap bar">
    <a class="brand" href="#home" aria-label="AuraAI home">
      <svg viewBox="0 0 24 24" fill="#3aa0ff"><path d="M12 1.5c.6 5.2 2.6 8.1 5.6 9.2 1.5.5 3.1.8 5 1.3-4.6 1-7.4 2.6-9 5.4-.7 1.2-1.2 3-1.6 5.6-.4-2.6-.9-4.4-1.6-5.6-1.6-2.8-4.4-4.4-9-5.4 1.9-.5 3.5-.8 5-1.3 3-1.1 5-4 5.6-9.2z" transform="translate(0 -.3)"/></svg>
      <b>Aura<span>AI</span></b><i>AI Career &amp; Skills Navigator</i>
    </a>
    <button class="menu" id="menu" aria-label="Toggle menu" aria-expanded="false">&#9776;</button>
    <nav id="nav">
      <a class="link active" href="#home">Home</a>
      <a class="link" href="#about">About</a>
      <a class="link" href="#contact">Contact</a>
      <div class="nav-actions">
        <a class="btn" href="#" data-route="login">Login</a>
        <a class="btn primary" href="#" data-route="register">Register</a>
      </div>
    </nav>
  </div>
</header>

<main id="home">
  <div class="wrap">
    <div class="hero">
      <div>
        <span class="badge">&#10022; Your AI Career Coach</span>
        <h1>Navigate your next move with <em>clarity.</em></h1>
        <p class="lead">AI Career &amp; Skills Navigator helps you identify skill gaps, find free learning resources, and explore real-time job market trends, all in one place.</p>
        <a class="btn primary lg" href="#" data-route="chat">&#128172; Enter Aura</a>
      </div>
      <div class="portrait">
        <img src="aura_avatar.jpg" alt="Aura, your AI career coach">
        <div class="hello">
          <strong><svg viewBox="0 0 24 24" fill="#fff"><path d="M12 1.5c.6 5.2 2.6 8.1 5.6 9.2 1.5.5 3.1.8 5 1.3-4.6 1-7.4 2.6-9 5.4-.7 1.2-1.2 3-1.6 5.6-.4-2.6-.9-4.4-1.6-5.6-1.6-2.8-4.4-4.4-9-5.4 1.9-.5 3.5-.8 5-1.3 3-1.1 5-4 5.6-9.2z"/></svg>Hi, I'm Aura!</strong>
          <span>Your AI Career &amp; Skills Navigator</span>
        </div>
      </div>
    </div>

    <div class="features">
      <div class="feat"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg></div><h3>Find Skill Gaps</h3><p>Discover what skills to build next.</p></div>
      <div class="feat"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="3"/><rect x="9" y="9" width="6" height="6" rx="1" fill="currentColor"/></svg></div><h3>Learn for Free</h3><p>Get curated free resources &amp; courses.</p></div>
      <div class="feat"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M9 7h8v8"/></svg></div><h3>Market Trends</h3><p>Explore real-time job opportunities.</p></div>
      <div class="feat"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l9 9-9 9-9-9z"/><circle cx="12" cy="12" r="2.5" fill="currentColor"/></svg></div><h3>Build Your Future</h3><p>Get personalized career guidance.</p></div>
    </div>
  </div>
</main>

<section class="block" id="about">
  <div class="wrap">
    <h2>About AuraAI</h2>
    <p class="sub">Aura is an AI agent that reasons about your goals, retrieves relevant knowledge, uses tools, and checks with you before important decisions.</p>
    <div class="about-grid">
      <div class="card"><h3>Knowledge-backed answers</h3><p>Aura searches a curated career knowledge base using RAG with FAISS and MiniLM embeddings, so advice stays grounded.</p></div>
      <div class="card"><h3>Tools when needed</h3><p>Wikipedia, DuckDuckGo search, an approved HTTP request tool and a calculator, used only when they help answer your question.</p></div>
      <div class="card"><h3>You stay in control</h3><p>For important choices Aura asks you to approve, reject or request another approach before it continues.</p></div>
    </div>
  </div>
</section>

<section class="block" id="contact">
  <div class="wrap contact-grid">
    <div>
      <h2>Contact us</h2>
      <p class="sub">Questions, feedback or ideas for Aura? Send a message and we will reply by email.</p>
      <div class="info">
        <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>support@auraai.example</div>
        <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>Chakwal, Punjab, Pakistan</div>
      </div>
    </div>
    <form id="contactForm">
      <label>Name<input required placeholder="Your name"></label>
      <label>Email<input type="email" required placeholder="you@example.com"></label>
      <label>Message<textarea required placeholder="How can we help?"></textarea></label>
      <button class="btn primary" type="submit">Send message</button>
      <p class="ok" id="ok">Message sent. We will get back to you soon.</p>
    </form>
  </div>
</section>

<footer>
  <div class="wrap foot">
    <span>&copy; <span id="yr">2026</span> AuraAI. All rights reserved.</span>
    <nav>
      <a href="#home">Home</a><a href="#about">About</a><a href="#contact">Contact</a>
    </nav>
  </div>
</footer>

<script>
document.getElementById('yr').textContent = new Date().getFullYear();

// Mobile menu
const nav = document.getElementById('nav'), menu = document.getElementById('menu');
menu.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menu.setAttribute('aria-expanded', open);
});
nav.addEventListener('click', e => { if (e.target.closest('a')) nav.classList.remove('open'); });

// Highlight the nav button for the section in view
const links = [...document.querySelectorAll('nav a.link')];
const targets = ['home','about','contact'].map(id => document.getElementById(id));
const io = new IntersectionObserver(entries => {
  entries.forEach(en => {
    if (en.isIntersecting) {
      links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + en.target.id));
    }
  });
}, { rootMargin: '-45% 0px -50% 0px' });
targets.forEach(t => io.observe(t));

// Placeholder routes: wire these to your pages in the Streamlit port
document.querySelectorAll('[data-route]').forEach(a =>
  a.addEventListener('click', e => { e.preventDefault(); console.log('Route:', a.dataset.route); }));

// Contact form (front-end only)
document.getElementById('contactForm').addEventListener('submit', e => {
  e.preventDefault();
  document.getElementById('ok').style.display = 'block';
  e.target.reset();
});
</script>
</body>
</html>

components.html(aura_html, height=880, scrolling=False)
