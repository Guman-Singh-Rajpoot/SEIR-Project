# Import required libraries
import sys                      
import requests                 
from bs4 import BeautifulSoup   
import re                       
from collections import Counter 
# This function converts a word into a numeric hash value

def rolling_hash(word, p=53, m=2**64):
    h = 0
    power = 1
    
    for ch in word:
        # Convert character to ASCII and multiply with power
        h = (h + ord(ch) * power) % m
        power = (power * p) % m
    
    return h



# This function generates a 64-bit fingerprint of a webpage

def simhash(freq):
    bits = [0] * 64   # Store weight of each bit
    
    for word, count in freq.items():
        h = rolling_hash(word)  # Get hash of each word
        
        for i in range(64):
            # If bit is 1, add weight; if 0, subtract weight
            if (h >> i) & 1:
                bits[i] += count
            else:
                bits[i] -= count

    # Create final SimHash value
    final_hash = 0
    for i in range(64):
        if bits[i] > 0:
            final_hash |= (1 << i)

    return final_hash



def getwords(url):
    # Download webpage
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Get all text and convert to lowercase
    text = soup.get_text().lower()
    
    # Extract only words using regex
    words = re.findall(r'\w+', text)

    # Count frequency of each word
    return Counter(words)



# Check if user provided two URLs
if len(sys.argv) < 3:
    print("Usage: python Project2.py <URL1> <URL2>")
    exit()

# Take URLs from command line
url1 = sys.argv[1]
url2 = sys.argv[2]

print("Fetching pages... Please wait")

# Get word frequencies for both URLs
freq1 = getwords(url1)
freq2 = getwords(url2)

# Generate SimHash for both pages
hash1 = simhash(freq1)
hash2 = simhash(freq2)

# Count different bits between two hashes
diff_bits = bin(hash1 ^ hash2).count("1")
common_bits = 64 - diff_bits

# Print results
print("\nSimHash of URL1 =", hash1)
print("SimHash of URL2 =", hash2)
print("Common bits =", common_bits, "/ 64")