import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_blog_links_env(soup):
    # Adjust the selector to match the links to the blog posts on the website
    #it returns a list of the block links
    blog_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'en/blog/' in href and href not in blog_links:
            blog_links.append(href)
    return blog_links



def beautiful_soup_scrape_url(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup
