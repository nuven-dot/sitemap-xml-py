import os
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import time
from xml.dom import minidom

# List of user-agent strings to rotate through
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
]

# Function to select a random user-agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)

# Function to check if a URL is valid
def is_valid_url(url):
    try:
        parsed_url = urlparse(url)
        return bool(parsed_url.scheme and parsed_url.netloc)
    except Exception:
        return False

# Function to scrape a URL with retries and rotating user-agents
def fetch_with_retries(url, max_retries=2):
    attempt = 0
    while attempt <= max_retries:
        user_agent = get_random_user_agent()
        headers = {'User-Agent': user_agent}
        print(f"Attempt {attempt + 1}: Fetching {url} with User-Agent: {user_agent}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"Success: Retrieved {url} (Status: {response.status_code})")
                return response.text
            elif response.status_code == 403:
                print(f"Forbidden: Status 403, trying again with a different User-Agent...")
            else:
                print(f"Failed: Status {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
        
        attempt += 1
        time.sleep(2)  # Wait before retrying
    print(f"Failed to retrieve {url} after {max_retries + 1} attempts.")
    return None

# Function to scrape and collect URLs from a website
def scrape_urls(base_url, max_depth=3):
    visited = set()  # To avoid visiting the same URL multiple times
    urls_to_visit = {base_url}
    all_urls = set()

    # Crawl up to the specified depth
    for depth in range(max_depth):
        print(f"Depth {depth + 1}: Found {len(urls_to_visit)} URLs to crawl.")
        current_urls = urls_to_visit.copy()
        urls_to_visit.clear()

        for url in current_urls:
            if url not in visited:
                visited.add(url)
                html_content = fetch_with_retries(url)
                if html_content:
                    soup = BeautifulSoup(html_content, 'lxml')  # Use lxml for better parsing
                    # Find all anchor tags
                    for link in soup.find_all('a', href=True):
                        # Join the base URL with the relative link
                        new_url = urljoin(base_url, link['href'])
                        # Keep only URLs that belong to the same domain
                        if is_internal_url(base_url, new_url):
                            all_urls.add(new_url)
                            if new_url not in visited:
                                urls_to_visit.add(new_url)
    return all_urls

# Function to check if a URL belongs to the same domain (internal)
def is_internal_url(base_url, new_url):
    base_domain = urlparse(base_url).netloc
    new_domain = urlparse(new_url).netloc
    return base_domain == new_domain

# Function to prettify the XML (add indentation)
def prettify_xml(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Function to create or update the sitemap
def create_sitemap(urls, base_url):
    # Create the <urlset> XML element
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for url in urls:
        url_element = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_element, "loc")
        loc.text = url
        lastmod = ET.SubElement(url_element, "lastmod")
        lastmod.text = time.strftime("%Y-%m-%d")  # Add current date as last modification date

    # Extract the domain name to create/update the folder
    domain_name = urlparse(base_url).netloc
    directory = domain_name

    # Check if the folder exists or create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    sitemap_filename = os.path.join(directory, "sitemap.xml")
    
    # Pretty-print and save the XML file
    with open(sitemap_filename, "w", encoding="utf-8") as f:
        f.write(prettify_xml(urlset))

    print(f"Sitemap updated and saved as {sitemap_filename}")

# Function to load URLs from a .txt file
def load_urls_from_txt(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines() if is_valid_url(line.strip())]
    return urls

# Main function to run the sitemap generator
def generate_sitemaps_from_file(file_path, max_depth=3):
    print(f"Loading URLs from {file_path}...")
    urls = load_urls_from_txt(file_path)

    for base_url in urls:
        print(f"Starting to scrape {base_url} to generate/update a sitemap...")
        found_urls = scrape_urls(base_url, max_depth=max_depth)
        print(f"Scraping completed for {base_url}. Found {len(found_urls)} URLs.")
        create_sitemap(found_urls, base_url)

# Execute the script
if __name__ == '__main__':
    txt_file = 'websites.txt'  # Replace with your .txt file containing URLs
    generate_sitemaps_from_file(txt_file, max_depth=3)
