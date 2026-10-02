import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="AuraAI | AI Career & Skills Navigator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State for Authentication & Navigation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"  # options: landing, auth, dashboard
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"  # login or register
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "user", "text": "What skills should I learn to become a Web Application Security Engineer?"},
        {"role": "aura", "text": "Great question! Becoming a Web Application Security Engineer requires a mix of technical skills, hands-on practice, and continuous learning."}
    ]
if "is_new_account" not in st.session_state:
    st.session_state.is_new_account = False

# Custom CSS matching your exact design system
st.markdown("""
<style>
:root {
  --bg-0: #030a1f; --bg-1: #061a45; --bg-2: #0a2a6b;
  --panel: rgba(12, 34, 84, .55); --panel-solid: #0b2253;
  --line: rgba(77, 140, 255, .28);
  --blue: #1f8bff; --blue-d: #1468d6; --cyan: #22e0c0; --violet: #b07cff;
  --text: #f2f6ff; --muted: #9db4dd;
}
.stApp {
  background: radial-gradient(900px 500px at 85% 12%, rgba(31,139,255,.28), transparent 60%),
              radial-gradient(700px 500px at 5% 0%, rgba(20,104,214,.25), transparent 60%),
              linear-gradient(160deg, var(--bg-0) 0%, var(--bg-1) 55%, #08235a 100%);
  color: var(--text);
  font-family: 'Plus Jakarta Sans', sans-serif;
}
/* Hide default Streamlit header/footer elements for custom immersive look */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ROUTE 1: LANDING PAGE
# ---------------------------------------------------------
if st.session_state.current_page == "landing":
    col1, col2, col3 = st.columns([2, 5, 2])
    with col1:
        st.markdown("### ✨ Aura<span>AI</span>", unsafe_allow_html=True)
    with col3:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Login", key="landing_login"):
                st.session_state.auth_mode = "login"
                st.session_state.current_page = "auth"
                st.rerun()
        with b2:
            if st.button("Register", key="landing_reg", type="primary"):
                st.session_state.auth_mode = "register"
                st.session_state.current_page = "auth"
                st.rerun()

    st.markdown("---")
    
    hero_col1, hero_col2 = st.columns(2)
    with hero_col1:
        st.markdown("<span style='color:#7db8ff; background:rgba(31,139,255,.08); padding:8px 18px; border-radius:999px; border:1px solid rgba(77,140,255,.28); font-weight:600;'>✨ Your AI Career Coach</span>", unsafe_allow_html=True)
        st.markdown("# Navigate your next move with <span style='color:#3aa0ff;'>clarity.</span>", unsafe_allow_html=True)
        st.markdown("<p style='color:#9db4dd; font-size:1.12rem;'>AI Career & Skills Navigator helps you identify skill gaps, find free learning resources, and explore real-time job market trends, all in one place.</p>", unsafe_allow_html=True)
        if st.button("💬 Enter Aura", type="primary", use_container_width=True):
            st.session_state.current_page = "auth"
            st.rerun()
            
    with hero_col2:
        st.info("💡 **Tip:** Register a new account to experience a personalized dashboard with a 0% starting progress track ready for your career roadmap!")

    st.markdown("<br><br>", unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown("### 🎯 Find Skill Gaps\nDiscover what skills to build next.")
    with f2:
        st.markdown("### 📚 Learn for Free\nGet curated free resources & courses.")
    with f3:
        st.markdown("### 📈 Market Trends\nExplore real-time job opportunities.")
    with f4:
        st.markdown("### 🚀 Build Your Future\nGet personalized career guidance.")

    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#9db4dd;'>&copy; 2026 AuraAI. All rights reserved. | Built with CrewAI & Groq</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ROUTE 2: AUTHENTICATION MODAL / PAGE
# ---------------------------------------------------------
elif st.session_state.current_page == "auth":
    st.markdown("<div style='max-width: 440px; margin: 40px auto; background: linear-gradient(170deg,#0d2a66,#071a45); padding: 30px; border-radius: 22px; border: 1px solid rgba(77,140,255,.28);'>", unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.current_page = "landing"
        st.rerun()

    auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
    
    with auth_tab1:
        st.subheader("Welcome back")
        login_email = st.text_input("Email", placeholder="you@example.com", key="login_email")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In", type="primary", use_container_width=True):
            if login_email:
                st.session_state.logged_in = True
                st.session_state.user_email = login_email
                st.session_state.user_name = login_email.split('@')[0].capitalize()
                st.session_state.is_new_account = False
                st.session_state.current_page = "dashboard"
                st.rerun()
            else:
                st.error("Please enter a valid email.")

    with auth_tab2:
        st.subheader("Create your account")
        reg_name = st.text_input("Full Name", placeholder="Your full name")
        reg_email = st.text_input("Email", placeholder="you@example.com", key="reg_email")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Create Account", type="primary", use_container_width=True):
            if reg_email and reg_name:
                st.session_state.logged_in = True
                st.session_state.user_email = reg_email
                st.session_state.user_name = reg_name
                st.session_state.is_new_account = True
                st.session_state.current_page = "dashboard"
                st.rerun()
            else:
                st.error("Please fill in all fields.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ROUTE 3: DASHBOARD
# ---------------------------------------------------------
elif st.session_state.current_page == "dashboard":
    t_col1, t_col2 = st.columns([6, 1])
    with t_col1:
        st.markdown("### ✨ AuraAI &nbsp;|&nbsp; <span style='font-size:0.9rem; color:#9db4dd;'>AI Career & Skills Navigator</span>", unsafe_allow_html=True)
    with t_col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.current_page = "landing"
            st.rerun()

    st.markdown("---")

    dash_col1, dash_col2, dash_col3 = st.columns([2.2, 5, 2.8])

    with dash_col1:
        st.markdown("#### Navigation")
        if st.button("💬 Chat with Aura", use_container_width=True, type="primary"):
            pass
        if st.button("🗺️ Career Roadmap", use_container_width=True):
            st.info("Roadmap view loaded.")
        if st.button("🎯 Skills Analysis", use_container_width=True):
            st.info("Skills module loaded.")
        if st.button("💼 Opportunities", use_container_width=True):
            st.info("Job market module loaded.")
        if st.button("📚 Resources", use_container_width=True):
            st.info("Learning resources loaded.")

        st.markdown("---")
        
        progress_val = 0 if st.session_state.is_new_account else 68
        st.markdown(f"#### Your Progress\n**Career Growth Journey: {progress_val}%**")
        st.progress(progress_val / 100)
        if st.session_state.is_new_account:
            st.caption("🌱 New account detected! Complete your first chat prompt to start building your roadmap.")

        st.markdown("---")
        st.markdown("#### Recent Chats")
        st.button("🔒 Web Application Security", use_container_width=True)
        st.button("📖 Free Learning Resources", use_container_width=True)

    with dash_col2:
        st.markdown("### 💬 Chat with Aura <span style='font-size:0.8rem; color:#22e0c0; float:right;'>● Aura is online</span>", unsafe_allow_html=True)
        
        chat_container = st.container(height=450)
        with chat_container:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.chat_message("user").write(message["text"])
                else:
                    st.chat_message("assistant", avatar="✨").write(message["text"])

        user_input = st.chat_input("Type your message to Aura...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            response_text = f"Analyzing your request regarding '{user_input}' using Groq GPT-OSS-120B and RAG vector search..."
            st.session_state.chat_history.append({"role": "aura", "text": response_text})
            if st.session_state.is_new_account:
                st.session_state.is_new_account = False
            st.rerun()

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📊 90-day Roadmap"):
                st.session_state.chat_history.append({"role": "user", "text": "Show me a 90-day roadmap"})
                st.session_state.chat_history.append({"role": "aura", "text": "Here is your customized 90-day milestone plan..."})
                st.rerun()
        with c2:
            if st.button("🔍 Free Resources"):
                st.session_state.chat_history.append({"role": "user", "text": "Find free learning resources"})
                st.session_state.chat_history.append({"role": "aura", "text": "Curated free courses and labs retrieved from RAG database."})
                st.rerun()
        with c3:
            if st.button("💼 Job Opportunities"):
                st.session_state.chat_history.append({"role": "user", "text": "Explore job opportunities"})
                st.session_state.chat_history.append({"role": "aura", "text": "Searching live market API for relevant roles..."})
                st.rerun()

    with dash_col3:
        st.markdown(f"### Profile: {st.session_state.user_name}")
        st.markdown(f"<p style='color:#9db4dd; font-size:0.85rem;'>{st.session_state.user_email}</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("#### ⚡ System Intelligence")
        st.markdown("- **Model:** Groq GPT-OSS-120B")
        st.markdown("- **Knowledge Base:** FAISS + Sentence Transformers")
        st.markdown("- **Tools:** Search, Wikipedia, API, Calculator")
        st.markdown("- **Security:** OWASP LLM Guardrails")
        
        st.markdown("---")
        st.markdown("> *&ldquo;Big dreams need a plan. I'm here to help you build yours.&rdquo;* — **Aura**")
