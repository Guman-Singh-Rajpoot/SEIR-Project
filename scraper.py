import sys
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from itertools import combinations
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_word_freq(text):
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def rolling_hash(word, p=53, m=2**64):
    h = 0
    power = 1
    for ch in word:
        h = (h + ord(ch) * power) % m
        power = (power * p) % m
    return h

def find_simhash(word_freq):
    vector = [0] * 64

    for word, freq in word_freq.items():
        h = rolling_hash(word)
        for i in range(64):
            bit = (h >> i) & 1
            if bit:
                vector[i] += freq
            else:
                vector[i] -= freq

    simhash = 0
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)

    return simhash

def fetch_page(url):
    print("\n" + "="*60)
    print("URL:", url)
    print("="*60)

    try:
        response = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        print("\nPage Title:")
        title = soup.title.string if soup.title else "No Title Found"
        print(title)

        print("\nPage Body Text (First 1000 chars):")
        body_text = soup.get_text(separator=" ", strip=True)
        print(body_text[:1000])

        print("\nAll URLs on Page:")
        links = set()
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                links.add(href)

        for l in links:
            print(l)

        word_freq = find_word_freq(body_text)
        simhash = find_simhash(word_freq)

        print("\nSimhash:", simhash)
        return simhash

    except Exception as e:
        print("Error fetching page:", e)
        return None

if len(sys.argv) < 2:
    print("Usage:")
    print("  python SEIR_Project.py <URL1>")
    print("  python SEIR_Project.py <URL1> <URL2>")
    print("  python SEIR_Project.py <URL1> <URL2> <URL3> ...")
    sys.exit()

urls = sys.argv[1:]
hashes = {}

# Fetch all URLs
for url in urls:
    simhash = fetch_page(url)
    if simhash is not None:
        hashes[url] = simhash

# If only one website
if len(hashes) == 1:
    print("\nOnly one website provided.")
    print("Simhash already displayed above.")

# If two or more websites → compare all pairs
elif len(hashes) >= 2:
    print("\n" + "="*60)
    print("SIMHASH COMPARISON RESULTS")
    print("="*60)

    for (url1, hash1), (url2, hash2) in combinations(hashes.items(), 2):
        common_bits = 64 - bin(hash1 ^ hash2).count("1")
        similarity_percentage = (common_bits / 64) * 100

        print(f"\nComparing:")
        print(f"{url1}")
        print(f"{url2}")
        print(f"Common Bits: {common_bits}/64")
        print(f"Similarity: {similarity_percentage:.2f}%")