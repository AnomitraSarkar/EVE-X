import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

def summarize_with_ollama(text, model="llama3.2"):
    url = "http://localhost:11434/api/generate"
    prompt = f"Summarize the following content:\n\n{text[:8000]}"  # truncate for safety
    response = requests.post(url, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

# Example usage
site = Website("https://tcs.com")  # Replace with the actual URL you want to summarize
summary = summarize_with_ollama(site.text)
print(f"Title: {site.title}\n\nSummary:\n{summary}")
