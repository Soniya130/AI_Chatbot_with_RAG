# utils/websearch_utils.py

from duckduckgo_search import DDGS

def web_search(query, max_results=3):
    """Perform a DuckDuckGo search and return results."""
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(r["body"])
        return results
    except Exception as e:
        return [f"Error fetching web results: {str(e)}"]
