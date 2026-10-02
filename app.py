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
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AuraAI — AI Career & Skills Navigator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b0f19; color: #f8fafc; margin: 0; padding: 0; }
        .glass-panel { background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .gradient-text { background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .glow-btn { box-shadow: 0 0 25px rgba(59, 130, 246, 0.4); transition: all 0.3s ease; }
        .glow-btn:hover { box-shadow: 0 0 35px rgba(6, 182, 212, 0.6); transform: translateY(-1px); }
    </style>
</head>
<body class="bg-[#0b0f19] text-slate-100 min-h-screen flex flex-col">

    <!-- Header -->
    <header class="glass-panel border-b border-slate-800 sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
        <div class="flex items-center space-x-3 cursor-pointer" onclick="switchView('landing')">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center glow-btn">
                <i class="fa-solid fa-atom text-white text-xl"></i>
            </div>
            <div>
                <h1 class="font-bold text-lg tracking-wide text-white flex items-center gap-2">
                    Aura<span class="text-cyan-400">AI</span>
                </h1>
                <p class="text-xs text-slate-400">AI Career & Skills Navigator</p>
            </div>
        </div>
        <nav class="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
            <a href="#" onclick="switchView('landing')" class="hover:text-cyan-400 transition">Home</a>
            <a href="#" onclick="switchView('dashboard')" class="hover:text-cyan-400 transition">Dashboard</a>
            <a href="#" onclick="switchView('about')" class="hover:text-cyan-400 transition">About</a>
            <a href="#" onclick="switchView('contact')" class="hover:text-cyan-400 transition">Contact</a>
        </nav>
        <div class="flex items-center space-x-4">
            <button onclick="switchView('dashboard')" class="px-5 py-2 text-sm font-semibold rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white glow-btn">Launch App</button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-grow p-4 md:p-6 max-w-[1700px] mx-auto w-full">
        <!-- Landing View -->
        <div id="view-landing" class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center py-12">
            <div>
                <span class="px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-cyan-400 border border-cyan-500/20">
                    <i class="fa-solid fa-sparkles mr-1"></i> Powered by CrewAI & Groq (GPT-OSS-120B)
                </span>
                <h2 class="text-4xl lg:text-5xl font-extrabold tracking-tight mt-6 leading-tight">
                    Navigate your next move with <span class="gradient-text">clarity</span>.
                </h2>
                <p class="text-slate-400 mt-4 text-lg">
                    Advanced AI-agent career guidance, RAG knowledge retrieval, and tailored skill roadmaps designed for your professional success.
                </p>
                <div class="mt-8 flex items-center gap-4">
                    <button onclick="switchView('dashboard')" class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold glow-btn">
                        Explore Aura AI <i class="fa-solid fa-arrow-right ml-2"></i>
                    </button>
                </div>
            </div>
            <div class="glass-panel p-6 rounded-2xl relative overflow-hidden border border-slate-700/50 shadow-2xl">
                <div class="flex items-center gap-4 mb-6">
                    <img src="https://raw.githubusercontent.com/Tajdar-Khalil/Goat-/main/aura_avatar.jpg" alt="Aura AI" class="w-16 h-16 rounded-full object-cover border-2 border-cyan-400 shadow-lg">
                    <div>
                        <h3 class="font-bold text-lg text-white flex items-center gap-2">
                            Aura <span class="px-2 py-0.5 text-[10px] rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Online</span>
                        </h3>
                        <p class="text-xs text-slate-400">Your AI Career Coach & Guide[cite: 2]</p>
                    </div>
                </div>
                <div class="space-y-3 text-sm text-slate-300">
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-between">
                        <span>Model Engine</span><span class="text-cyan-400 font-medium">GPT-OSS-120B[cite: 1]</span>
                    </div>
                    <div class="p-3 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-between">
                        <span>Knowledge Base</span><span class="text-cyan-400 font-medium">FAISS Vector DB & RAG[cite: 1]</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Dashboard View (Exact Reference Replica) -->
        <div id="view-dashboard" class="hidden grid-cols-1 xl:grid-cols-12 gap-6 py-4">
            <!-- Sidebar -->
            <div class="xl:col-span-3 glass-panel p-5 rounded-2xl flex flex-col justify-between h-[82vh]">
                <div class="space-y-6">
                    <div class="space-y-1">
                        <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-blue-600/20 text-cyan-400 font-semibold border border-blue-500/30">
                            <i class="fa-solid fa-comments"></i> Chat with Aura
                        </button>
                        <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 transition">
                            <i class="fa-solid fa-route"></i> Career Roadmap
                        </button>
                        <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-slate-400 hover:bg-slate-800/50 hover:text-slate-200 transition">
                            <i class="fa-solid fa-chart-pie"></i> Skills Analysis
                        </button>
                    </div>
                    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="flex justify-between text-xs mb-2">
                            <span class="text-slate-400">Career Growth Journey</span>
                            <span class="text-cyan-400 font-bold">68%</span>
                        </div>
                        <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                            <div class="bg-gradient-to-r from-blue-500 to-cyan-400 h-full w-[68%]"></div>
                        </div>
                    </div>
                </div>
                <div class="pt-4 border-t border-slate-800 text-xs text-slate-500 text-center">
                    Student ID: STU-456 | VU Pakistan
                </div>
            </div>

            <!-- Main Chat Interface -->
            <div class="xl:col-span-6 glass-panel p-6 rounded-2xl flex flex-col h-[82vh] justify-between">
                <div class="flex items-center justify-between pb-4 border-b border-slate-800">
                    <div>
                        <h3 class="font-bold text-white">Chat with Aura</h3>
                        <p class="text-xs text-slate-400">Your AI Career Coach[cite: 2]</p>
                    </div>
                    <span class="px-3 py-1 rounded-full text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Aura is online[cite: 2]
                    </span>
                </div>
                <div class="flex-grow overflow-y-auto space-y-4 py-4 pr-2">
                    <div class="flex items-start gap-3">
                        <img src="https://raw.githubusercontent.com/Tajdar-Khalil/Goat-/main/aura_avatar.jpg" class="w-8 h-8 rounded-full object-cover border border-cyan-400 mt-1">
                        <div class="bg-slate-800/80 border border-slate-700/60 p-4 rounded-2xl rounded-tl-none max-w-xl text-sm space-y-2">
                            <p class="text-slate-200">Hello Tajdar! I am Aura, your AI career coach powered by CrewAI and Groq LLM[cite: 1, 2]. How can I help you navigate your Data Science studies or cybersecurity career path today?</p>
                        </div>
                    </div>
                </div>
                <div class="pt-3 border-t border-slate-800 flex items-center gap-3">
                    <input type="text" id="chat-input" placeholder="Type your message to Aura..." class="flex-grow bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 focus:outline-none focus:border-cyan-500">
                    <button onclick="alert('Message sent to Aura agent!')" class="w-12 h-12 rounded-xl bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center transition glow-btn">
                        <i class="fa-solid fa-paper-plane"></i>
                    </button>
                </div>
            </div>

            <!-- Right Assistant Panel -->
            <div class="xl:col-span-3 glass-panel p-5 rounded-2xl flex flex-col justify-between h-[82vh]">
                <div class="space-y-6 text-center">
                    <img src="https://raw.githubusercontent.com/Tajdar-Khalil/Goat-/main/aura_avatar.jpg" class="w-24 h-24 rounded-full object-cover mx-auto border-2 border-cyan-400 shadow-xl">
                    <div>
                        <h3 class="font-bold text-white flex items-center justify-center gap-1.5">
                            Aura <span class="px-1.5 py-0.5 text-[9px] bg-blue-500/20 text-cyan-400 rounded">AI</span>[cite: 2]
                        </h3>
                        <p class="text-xs text-slate-400">Your Career Coach & Guide[cite: 2]</p>
                    </div>
                    <div class="space-y-2 text-left text-xs">
                        <div class="p-2.5 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-between">
                            <span class="text-slate-400">Model Engine</span><span class="text-cyan-400 font-semibold">GPT-OSS-120B[cite: 1]</span>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-between">
                            <span class="text-slate-400">Knowledge Base</span><span class="text-cyan-400 font-semibold">FAISS RAG[cite: 1]</span>
                        </div>
                    </div>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/40 border border-slate-800/80 text-center italic text-xs text-slate-400">
                    "Big dreams need a plan. I'm here to help you build yours." — Aura[cite: 2]
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="glass-panel border-t border-slate-800 py-6 text-center text-xs text-slate-400 mt-auto">
        © 2026 AuraAI — AI Career Skills Navigator. All rights reserved. Designed & developed by Tajdar Khalil.
    </footer>

    <script>
        function switchView(viewName) {
            ['landing', 'dashboard', 'about', 'contact'].forEach(v => {
                const el = document.getElementById('view-' + v);
                if (el) { el.classList.add('hidden'); el.classList.remove('grid'); }
            });
            const target = document.getElementById('view-' + viewName);
            if (target) {
                target.classList.remove('hidden');
                if(viewName === 'dashboard') { target.classList.add('grid'); }
            }
            window.scrollTo(0, 0);
        }
        switchView('dashboard');
    </script>
</body>
</html>
"""

components.html(aura_html, height=880, scrolling=False)
