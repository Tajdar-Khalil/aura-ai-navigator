from duckduckgo_search import DDGS
import wikipedia

def search_web(query):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=3)]
    return results

def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        return "No Wikipedia summary found."

def calculate(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid calculation expression."

def http_request(url):
    import requests
    response = requests.get(url, timeout=5)
    return response.text[:500]
