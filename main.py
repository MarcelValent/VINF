# Importing necessary libraries
import os
import requests
import re
import time
from urllib.parse import urljoin
from collections import deque
from bs4 import BeautifulSoup

# Base URL for the web scraping
base_url = 'https://www.nikeliga.sk/timy'
base2 = 'https://www.nikeliga.sk'


# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Function to write links to a text file
def write_links_to_txt(links, filename, mode='a'):
    with open(filename, mode, encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')


# Function to check if a link is valid based on keywords
def is_valid_link(link):
    keywords = ['tim', 'zapas', 'hrac']
    return any(keyword in link for keyword in keywords)


# Function to extract links from HTML content using BeautifulSoup
def extract_links_from_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
    return links


# Function to save HTML content to a file
def save_html_content(url, html_content, output_directory):
    subpage_name = url.split("/")[-1].split("?")[0].replace(".html", "")
    filename = os.path.join(output_directory, subpage_name + ".html")
    with open(filename, "w", encoding='utf-8') as f:
        f.write(html_content)


# Function to scrape subpages recursively
def scrape_subpages(url, output_directory, queue, visited):
    if url in visited:
        return

    print(f"Scraping {url}")

    # Sending a request to the URL
    response = requests.get(url, headers={'User-Agent': 'WebScraper for University project: Mozilla/5.0'})
    if not response.ok:
        print(f"Failed to retrieve: {url}")
        return

    html_content = response.text

    # Marking the URL as visited
    visited.add(url)

    # Extracting links from the page and adding to the queue
    links_on_page = extract_links_from_page(html_content)
    for link in links_on_page:
        absolute_url = urljoin(base2, link)
        if absolute_url.startswith(base2) and is_valid_link(absolute_url):
            queue.append(absolute_url)

    # Saving HTML content to a file
    save_html_content(url, html_content, output_directory)

    time.sleep(2)  # Adjust the time delay to be respectful to the website


# Main recursive crawler function
def recursive_crawler(starting_url, output_directory='nikeliga_data'):
    # Creating the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Setting the path for the file containing existing links
    output_file = os.path.join(output_directory, "existing_links.txt")

    # Initializing the queue and visited set
    queue = deque()
    visited = set()

    # Clearing the existing links file
    with open(output_file, "w") as f:
        f.write('')

    # Reading existing links from the file if it exists
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            visited = set(line.strip() for line in f.readlines())

    # Adding the starting URL to the queue
    queue.append(starting_url)

    # Main crawling loop
    while queue:
        url = queue.popleft()
        scrape_subpages(url, output_directory, queue, visited)

    print("Scraping completed.")


# Entry point of the script
if __name__ == "__main__":
    # Calling the recursive crawler with the base URL
    recursive_crawler(base_url, output_directory='nikeliga_data')
