
import requests

def search_wikipedia(query: str):
    try:
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            headers={
                "User-Agent": "AgenticAIProject/1.0 (your_email_here)"
            },
            params={
                "action": "query",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "titles": query,
                "format": "json"
            }
        )

        if response.status_code != 200:
            return f"HTTP Error {response.status_code}"

        data = response.json()
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))

        return page.get("extract", "No result found.") or "No result found."

    except Exception as e:
        return f"Error: {str(e)}"