# Import required modules
import sys                     # Used to take input from command line
import requests                # Used to fetch website data
from bs4 import BeautifulSoup  # Used to extract HTML content easily


# Main function
def main():
    
    # Check if user gave exactly one URL
    if len(sys.argv) != 2:
        print("Usage: python project1.py <URL>")
        return

    # Get the URL from command line
    url = sys.argv[1]

    # If user did not type http/https, add https automatically
    if not url.startswith("http"):
        url = "https://" + url

    # Send request to website and get HTML code
    response = requests.get(url)
    html = response.text

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Get webpage title
    title = soup.title.string if soup.title else "No Title"
    print("TITLE:\n", title)

    # Extract all text from webpage body
    body_text = soup.get_text(separator="\n", strip=True)
    print("\nBODY TEXT:\n", body_text)

    # Extract all hyperlinks from webpage
    print("\nLINKS:")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            print(href)


# Run main function only when file is executed directly
if __name__ == "__main__":
    main()