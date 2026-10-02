import os
import google.generativeai as genai
from tools import search_web, search_wikipedia, calculate, http_request

class AuraAgent:
    def __init__(self, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        with open("system_prompt.txt", "r") as f:
            self.system_prompt = f.read()

    def run_agentic_workflow(self, user_query, conversation_history=""):
        prompt = f"""
        {self.system_prompt}
        
        Conversation History:
        {conversation_history}
        
        User Goal / Query: {user_query}
        
        Execute the agentic loop (Goal -> Decide -> Act -> Observe -> Complete) and provide a structured, professional response.
        """
        response = self.model.generate_content(prompt)
        return response.text
