import sys
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching the URL:", e)
        sys.exit(1)

def extract_data(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    # 1. Page Title
    title = soup.title.string.strip() if soup.title else "No Title Found"

    # 2. Page Body Text (no HTML tags)
    body_text = soup.get_text(separator="\n", strip=True)

    # 3. All URLs the page links to
    links = []
    for link in soup.find_all("a", href=True):
        links.append(link["href"])

    return title, body_text, links


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    html = fetch_page(url)
    title, body_text, links = extract_data(html, url)

    # Output (one per line section)
    print("----- PAGE TITLE -----")
    print(title)

    print("\n----- PAGE BODY TEXT -----")
    print(body_text)

    print("\n----- ALL LINKS -----")
    for link in links:
        print(link)


if __name__ == "__main__":
    main()