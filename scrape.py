import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

# List of URLs to scrape
urls_to_scrape = [
    "https://developer.android.com/develop/ui/compose/compositionlocal",
    "https://developer.android.com/develop/ui/compose/layering",
    "https://developer.android.com/develop/ui/compose/accessibility/semantics"
]

def generate_safe_filename(url):
    """Convert URL to safe filename"""
    parsed = urlparse(url)
    return f"{parsed.netloc}{parsed.path}".replace("/", "_").replace(".", "-") + ".txt"

def scrape_content_and_save(url):
    try:
        print(f"Scraping: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('main').get_text()  # Adjust selector per website
        
        # Create filename from URL
        filename = generate_safe_filename(url)
        filepath = os.path.join("docs", filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Saved: {filename}")
        
    except Exception as error:
        print(f"Failed to scrape {url}: {str(error)}")

# Create docs directory
os.makedirs("docs", exist_ok=True)

# Scrape all URLs
for url in urls_to_scrape:
    scrape_content_and_save(url)

print("Scraping completed!")