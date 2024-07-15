import requests
from bs4 import BeautifulSoup
import re
import spacy
import pandas as pd
from scraping_basic import extract_blog_links, beautiful_soup_scrape_url
from excel_save import save_to_excel

#this here would check if the blog post contains the keywords and return them to us
# now we will work on the search query
# Missing: fixing the companys urls
# Missing: fixing the search query
# Missing: fixing the keywords
# Missing: find the correct websites for each query


company_sites = [
    {
        "name": "ENVIRIA Energy Holding GmbH",
        "url": "https://enviria.energy/en/blog"
    },
    { 
        "name": "ENREGO Energy GmbH",
        "url": "https://enrego.de/"
    },
    {
        "name": "HIH Invest Real Estate Austria GmbH",
        "url": "https://hih-invest.de/en/press-releases/"
    },
    {
        "name": "Merkle Germany GmbH",
        "url": "https://www.merkle.com/en/home.html"
    },
]

#according to wikipidia, the following are the keywords that are used to describe solar parks
investment_keywords = ["solar park","solar farm",
                       "solar power plant","photovoltaic power station"]
watt_keywords = ["MW", "megawatt", "megawatts", "GW", "gigawatt", "gigawatts"]
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def scrape_blog_posts(base_url, blog_links):
    investment_infos = []
    #this is only taking the important hyperlinks in the body automatically
    
    for link in blog_links:
        #delete en/blog/ from the link and add the base url to get the full link
        link = link.replace('en/blog/', '')
        full_url = base_url + link if not link.startswith('http') else link
        soup = beautiful_soup_scrape_url(full_url)
        #extract the investment info from the blog post
        investment_info = extract_investment_info(soup)
        
        investment_infos.append({
            "url": full_url,
            "investment_info": investment_info
        })
    return investment_infos

def extract_investment_info(soup):
    text = soup.get_text()
    doc = nlp(text)

    investment_info = {
        "equity_checks": [],
        "megawatts": [],
        "investing_in_solar_parks": False
    }
    
    if any(term in text.lower() for term in investment_keywords):
        investment_info["investing_in_solar_parks"] = True

    # Perform named entity recognition
    #entities = extract_entities(visible_text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
 
    for entity, label in entities:
        if 'equity' in entity.lower() and label != 'ORG':
                investment_info["equity_checks"].append((entity, label))
            
        if any(term in entity.lower() for term in watt_keywords) and label == 'QUANTITY':
            investment_info["megawatts"].append((entity, label))
        #add the investment one to the list
    #return investment_info
    
    print(investment_info)
    
def main():
    results = []
    for company in company_sites:
        print(f"Scraping {company['name']}...")

        #get the reports or the news page of the company
        soup = beautiful_soup_scrape_url(company["url"])
        # get all the hyperlinks of the blog posts
        blog_links = extract_blog_links(soup)
        # ex of a blog link: "/en/blog/solar-package-1-how-companies-benefit-from-the-new-regulation" of enviria
        

        if blog_links:
            blog_investment_infos = scrape_blog_posts(company["url"], blog_links)
            results.append({
                "company": company["name"],
                "url": company["url"],
                "blog_investment_infos": blog_investment_infos
            })
        else:
            investment_info = extract_investment_info(soup)
            results.append({
                "company": company["name"],
                "url": company["url"],
                "investment_info": investment_info
            })
    # Save results to Excel
    save_to_excel(results)
    print("reached the end") 

if __name__ == "__main__":
    main()
