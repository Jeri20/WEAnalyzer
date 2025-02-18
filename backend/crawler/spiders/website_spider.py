from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def crawl_website(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()  # Get the page HTML
        browser.close()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Extract title, headings, and metadata
    title = soup.title.string if soup.title else "No title"
    headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]  # Extract h1, h2, h3
    metadata = {
        'description': soup.find('meta', {'name': 'description'}),
        'keywords': soup.find('meta', {'name': 'keywords'}),
    }

    return {
        'title': title,
        'headings': headings,
        'metadata': metadata,
    }
