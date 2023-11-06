import os
import requests
import re
import time
from urllib.parse import urljoin
from collections import deque
from bs4 import BeautifulSoup

# Base URL
base_url = 'https://www.nikeliga.sk/timy'
base2 = 'https://www.nikeliga.sk'

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_links_to_txt(links, filename, mode='a'):
    with open(filename, mode, encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')

def is_valid_link(link):
    keywords = ['tim', 'zapas', 'hrac']
    return any(keyword in link for keyword in keywords)

def extract_links_from_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
    return links

def save_html_content(url, html_content, output_directory):
    subpage_name = url.split("/")[-1].split("?")[0].replace(".html", "")
    filename = os.path.join(output_directory, subpage_name + ".html")
    with open(filename, "w", encoding='utf-8') as f:
        f.write(html_content)

def scrape_subpages(url, output_directory, queue, visited):
    if url in visited:
        return

    print(f"Scraping {url}")

    response = requests.get(url, headers={'User-Agent': 'WebScraper for University project: Mozilla/5.0'})
    if not response.ok:
        print(f"Failed to retrieve: {url}")
        return

    html_content = response.text

    visited.add(url)

    links_on_page = extract_links_from_page(html_content)
    for link in links_on_page:
        absolute_url = urljoin(base2, link)
        if absolute_url.startswith(base2) and is_valid_link(absolute_url):
            queue.append(absolute_url)

    save_html_content(url, html_content, output_directory)

    time.sleep(2)  # Adjust the time delay to be respectful to the website

def recursive_crawler(starting_url, output_directory='nikeliga_data'):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = os.path.join(output_directory, "existing_links.txt")

    queue = deque()
    visited = set()

    with open(output_file, "w") as f:
        f.write('')
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            visited = set(line.strip() for line in f.readlines())

    queue.append(starting_url)

    while queue:
        url = queue.popleft()
        scrape_subpages(url, output_directory, queue, visited)

    print("Scraping completed.")

if __name__ == "__main__":
    recursive_crawler(base_url, output_directory='nikeliga_data')
