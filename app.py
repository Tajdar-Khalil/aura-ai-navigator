@@
 import base64
 import json
 import re
 from pathlib import Path
 
 import streamlit as st
 import streamlit.components.v1 as components
+
+from memory import ConversationMemory
@@
 HASH_PATTERN = re.compile(r"^[a-f0-9]{64}$")
+CHAT_MESSAGE_PARAM = "chat_message"
+CHAT_NONCE_PARAM = "chat_nonce"
@@
 def _init_session() -> None:
     st.session_state.setdefault("demo_users", {})
     st.session_state.setdefault("auth_user", None)
     st.session_state.setdefault("auth_feedback", None)
+    st.session_state.setdefault("chat_memory", ConversationMemory(max_turns=8))
+    st.session_state.setdefault("chat_history", [])
+    st.session_state.setdefault("chat_error", None)
+    st.session_state.setdefault("last_chat_nonce", None)
@@
 def _handle_auth_action() -> None:
@@
     st.rerun()
+
+
+def _clear_query_params(page: str = "dashboard") -> None:
+    """Remove one-shot action parameters while preserving the current page."""
+    st.query_params.clear()
+    st.query_params["page"] = page
+
+
+def _handle_chat_action() -> None:
+    """Process one dashboard chat message through the Python backend."""
+    if _current_page() != "dashboard":
+        return
+
+    message = _param(CHAT_MESSAGE_PARAM).strip()
+    nonce = _param(CHAT_NONCE_PARAM).strip()
+    if not message or not nonce:
+        return
+
+    # Prevent duplicate processing if the browser or Streamlit repeats a request.
+    if nonce == st.session_state.get("last_chat_nonce"):
+        _clear_query_params("dashboard")
+        st.rerun()
+
+    st.session_state["last_chat_nonce"] = nonce
+    st.session_state["chat_error"] = None
+    st.session_state["chat_history"].append({"role": "user", "content": message})
+    st.session_state["chat_memory"].add("user", message)
+
+    try:
+        from agent import run_aura
+        from rag import retrieve_context
+
+        retrieved_context = retrieve_context(message)
+        answer = run_aura(
+            user_query=message,
+            memory=st.session_state["chat_memory"],
+            retrieved_context=retrieved_context,
+            human_approved=False,
+        ).strip()
+
+        if not answer:
+            raise RuntimeError("Aura returned an empty response.")
+
+        st.session_state["chat_history"].append(
+            {"role": "assistant", "content": answer}
+        )
+        st.session_state["chat_memory"].add("assistant", answer)
+    except Exception as exc:
+        error_message = (
+            "Aura could not process that request right now. "
+            "Please check the backend configuration and try again."
+        )
+        st.session_state["chat_error"] = error_message
+        st.session_state["chat_history"].append(
+            {"role": "assistant", "content": error_message}
+        )
+        st.session_state["chat_memory"].add("assistant", error_message)
+        print(f"Aura chat error: {exc}")
+
+    _clear_query_params("dashboard")
+    st.rerun()
@@
 def _inject_navigation_and_assets(
     html: str,
     page: str,
     avatar_url: str,
     auth_user: dict[str, str] | None,
     auth_feedback: dict[str, str] | None,
+    chat_history: list[dict[str, str]],
+    chat_error: str | None,
 ) -> str:
@@
-    responsive_style = """
+    responsive_style = """
 <style>
-html, body { width: 100%; max-width: 100%; }
-body { margin: 0; }
-[data-testid="stAppViewContainer"] { overflow-x: hidden; }
+html, body {
+  width: 100%;
+  max-width: 100%;
+  min-width: 0;
+}
+body {
+  margin: 0;
+  overflow-x: hidden;
+}
 @media (max-width: 640px) {
-  .wrap { width: min(100%, calc(100% - 24px)) !important; }
+  .wrap {
+    width: min(100%, calc(100% - 24px)) !important;
+  }
 }
 </style>
 """
 
     dashboard_overrides = """
 <style>
-html, body { height: auto !important; min-height: 100% !important; }
-body { overflow: auto !important; }
-.app { gap: 14px !important; padding: 14px !important; min-height: calc(100vh - 64px); }
-aside.left, aside.right, .recent { overflow: visible !important; }
-.msgs { max-height: min(58vh, 680px); }
+html,
+body {
+  height: auto !important;
+  min-height: 100% !important;
+}
+body {
+  overflow: auto !important;
+}
+.app {
+  width: 100%;
+  min-height: calc(100vh - 64px);
+  grid-template-rows: minmax(0, 1fr);
+  gap: 14px !important;
+  padding: 14px !important;
+}
+main.chat {
+  min-width: 0;
+  min-height: 620px;
+}
+aside.left,
+aside.right,
+.recent {
+  min-width: 0;
+  overflow: visible !important;
+}
+.msgs {
+  min-height: 260px;
+  max-height: 58vh;
+}
+.bub {
+  overflow-wrap: anywhere;
+}
 @media (max-width: 860px) {
-  .top { padding: 0 12px !important; }
-  .app { padding: 10px !important; }
-  .msgs { max-height: none !important; padding: 14px !important; }
-  .chips { justify-content: flex-start !important; padding: 0 12px 12px !important; }
-  .input { margin: 0 12px 12px !important; }
+  .top {
+    height: auto !important;
+    min-height: 64px;
+    padding: 10px 12px !important;
+  }
+  .app {
+    display: block !important;
+    padding: 10px !important;
+  }
+  main.chat {
+    min-height: calc(100vh - 84px);
+  }
+  .msgs {
+    max-height: none !important;
+    min-height: 340px;
+    padding: 14px !important;
+  }
+  .chips {
+    justify-content: flex-start !important;
+    padding: 0 12px 12px !important;
+  }
+  .input {
+    margin: 0 12px 12px !important;
+  }
+  .c-head {
+    padding: 14px !important;
+  }
+  .online {
+    padding: 6px 9px !important;
+    font-size: .72rem !important;
+  }
+  .m {
+    max-width: 100%;
+  }
 }
 </style>
 """
@@
-    auth_json = json.dumps(auth_user or {})
-    feedback_json = json.dumps(auth_feedback or {})
+    auth_json = json.dumps(auth_user or {})
+    feedback_json = json.dumps(auth_feedback or {})
+    chat_json = json.dumps(chat_history or [])
+    chat_error_json = json.dumps(chat_error or "")
@@
 const __AURA_AUTH_USER = {auth_json};
 const __AURA_AUTHENTICATED = Boolean(__AURA_AUTH_USER && __AURA_AUTH_USER.email);
 const __AURA_FEEDBACK = {feedback_json};
+const __AURA_CHAT_HISTORY = {chat_json};
+const __AURA_CHAT_ERROR = {chat_error_json};
@@
 if (__AURA_PAGE === 'dashboard') {{
@@
   if (tools && !document.getElementById('logoutBtn')) {{
@@
     tools.appendChild(logoutButton);
   }}
+
+  window.__auraSubmitChat = function(message) {{
+    const cleanMessage = String(message || '').trim();
+    if (!cleanMessage) return;
+
+    const target = new URL(window.parent.location.href);
+    target.searchParams.set('page', 'dashboard');
+    target.searchParams.set('chat_message', cleanMessage);
+    target.searchParams.set('chat_nonce', `${{Date.now()}}-${{Math.random().toString(16).slice(2)}}`);
+    window.parent.location.href = target.toString();
+  }};
+
+  function __auraRenderChatHistory() {{
+    const messages = document.getElementById('msgs');
+    if (!messages || !Array.isArray(__AURA_CHAT_HISTORY) || !__AURA_CHAT_HISTORY.length) {{
+      return;
+    }}
+
+    messages.innerHTML = '';
+
+    __AURA_CHAT_HISTORY.forEach((item) => {{
+      const row = document.createElement('div');
+      const isUser = item.role === 'user';
+      row.className = `m${{isUser ? ' me' : ''}}`;
+
+      const avatar = isUser
+        ? '<div class="av"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" fill="#fff" stroke="none"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6" fill="#fff" stroke="none"/></svg></div>'
+        : '<img src="{avatar_url}" alt="Aura">';
+
+      const bubble = document.createElement('div');
+      bubble.className = 'bub';
+      bubble.textContent = item.content || '';
+
+      row.innerHTML = avatar;
+      row.appendChild(bubble);
+      messages.appendChild(row);
+    }});
+
+    messages.scrollTop = messages.scrollHeight;
+  }}
+
+  __auraRenderChatHistory();
+
+  if (__AURA_CHAT_ERROR) {{
+    console.warn(__AURA_CHAT_ERROR);
+  }}
 }}
 </script>
 """
@@
 _init_session()
 _handle_auth_action()
+_handle_chat_action()
@@
     rendered_html = _inject_navigation_and_assets(
         html_source,
         page,
         avatar_url,
         st.session_state.get("auth_user"),
         st.session_state.get("auth_feedback"),
+        st.session_state.get("chat_history", []),
+        st.session_state.get("chat_error"),
     )
     st.session_state["auth_feedback"] = None
-    components.html(rendered_html, height=900 if page == "dashboard" else 1200, scrolling=False)
+    components.html(
+        rendered_html,
+        height=980 if page == "dashboard" else 1280,
+        scrolling=True,
+    )
