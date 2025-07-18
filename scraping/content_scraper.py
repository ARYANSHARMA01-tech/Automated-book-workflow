import requests
from bs4 import BeautifulSoup

def fetch_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text(separator='\n', strip=True)
    return content