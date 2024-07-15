import feedparser
import csv
import spacy
from transformers import pipeline
from bs4 import BeautifulSoup
import requests
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json
from LLM import model_inference
from excel_save import save_to_excel_company
import time
#import neuralcoref

class GoogleNewsFeedScraper:
    def __init__(self, limit=3):
        self.limit = limit
        self.data = []
        self.nlp = spacy.load("en_core_web_sm")
        self.stemmer = PorterStemmer()
        self.solar_park_keywords = [self.stemmer.stem(word) for word in ["solar park", "solar farm", "solar power plant", "photovoltaic power station"]]
        self.watt_keywords = [self.stemmer.stem(word) for word in ["MW", "megawatt", "GW", "gigawatt"]]
        self.investment_keywords = [self.stemmer.stem(word) for word in ['investment', 'investor']]
        self.equity_keywords = [self.stemmer.stem(word) for word in ['equity', 'equities']]  

    def extract_investment_info(self, page_content):
        """Extracts investment information from a page using spaCy."""
        soup = BeautifulSoup(page_content, 'html.parser')
        soup = soup.find('body')
        text = soup.get_text(separator=' ')  # Use space as separator to avoid joining unrelated parts
        self.nlp = spacy.load("en_core_web_sm")
        doc = self.nlp(text)
        
        investment_info = {
            "equity_checks": [],
            "megawatts": [],
            "investing_in_solar_parks": False
        }

        words = word_tokenize(text)
        stemmed_words = [self.stemmer.stem(word) for word in words]
        stemmed_text = ' '.join(stemmed_words)
        stemmed_doc = self.nlp(stemmed_text)

        # Check if any solar park keywords are present in the stemmed text
        if not any(solar in stemmed_text for solar in self.solar_park_keywords):
            print("No solar park keywords found.")
            return investment_info  
        else:
            print("Solar park keywords were found.") 

        # Extract sentences containing investment keywords in the stemmed text
        investment_sentences = [sent for sent in doc.sents if any(self.stemmer.stem(term) in self.stemmer.stem(sent.text) for term in self.investment_keywords)]
        if investment_sentences:
            investment_info["investing_in_solar_parks"] = True

        # Extract relevant investment sentences
        for sent in investment_sentences:
            if any(ent.label_ == "MONEY" for ent in sent.ents):
                clean_text = ' '.join(sent.text.split())
                investment_info["equity_checks"].append(clean_text)

        # Check all sentences for the megawatts in the stemmed text
        megawatt_sentences = [sent for sent in doc.sents if any(self.stemmer.stem(term) in self.stemmer.stem(sent.text) for term in self.watt_keywords)]
        for sent in megawatt_sentences:
            if any(ent.label_ == "QUANTITY" for ent in sent.ents):
                clean_text = ' '.join(sent.text.split())
                investment_info["megawatts"].append(clean_text)

        return investment_info

    def extract_investment_info_using_LLM(self, page_content):
        """Extracts investment information from a page using the LLM model."""
        soup = BeautifulSoup(page_content, 'html.parser')
        soup = soup.find('body')
        # Using space as separator to avoid joining unrelated parts
        text = soup.get_text(separator=' ')  
        self.nlp = spacy.load("en_core_web_sm")
        doc = self.nlp(text)

        #check if the company is mentioned in the text if yes consider that company in the model
        companies = ["ENVIRIA" , "ENREGO", "HIH" , "Merkle"]
        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.label_))
        found_companies = []
        
        for company in companies:
            for entity, label in entities:
                if company in entity and company not in found_companies:
                    found_companies.append(company)
        if found_companies:
            return model_inference(text,found_companies)
        else:
            return {
            "equity_checks": [],
            "megawatts": [],
            "investing_in_solar_parks": False
        }
           
        
    
    def convert_to_rss_url(self, url):
        """Converts a Google News URL to an RSS feed URL."""
        if "https://news.google.com/search?" in url:
            url = url.replace("https://news.google.com/search?", "https://news.google.com/rss/search?")
            url = url.replace(" ", "%20")
            return url
        else:
            raise ValueError("Invalid URL.")
      
    def scrape_google_news_feed(self, url):
        
        feed = feedparser.parse(url)

        if feed.entries:
            num_entries = 0
            count=0
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                pubdate = entry.published
                try:
                    page_content = requests.get(link).text
                    investment_info = self.extract_investment_info(page_content)
                    count+=1
                    if count % 10 == 0:
                        print(f"Processed {count} articles.")
                    
                    if investment_info["investing_in_solar_parks"]:
                        num_entries += 1
                        
                        self.data.append({
                            "title": title,
                            "link": link,
                            "pubdate": pubdate,
                            "investment_info": investment_info
                        })
                    if count ==20:
                        break
                    if num_entries >= self.limit:
                        break
                    time.sleep(1) # Add a delay
                except requests.RequestException as e:
                    print(f"Error fetching page content: {e}")
                
        else:
            print("Nothing Found!")



def main():
    company_names = ['solar investing' ,"ENVIRIA" , "ENREGO", "HIH" , "Merkle","solar park", "solar farm", "solar power plant", "photovoltaic power station"]
    scraper = GoogleNewsFeedScraper()
    #
    for company_name in company_names:
        url = f"https://news.google.com/search?q={company_name}&hl=en-US&gl=US&ceid=US%3Aen"
        rss_url = scraper.convert_to_rss_url(url)
        scraper.scrape_google_news_feed(rss_url)
    
    print("Scraping completed.")
    print(f'len(scraper.data): {len(scraper.data)}')

    #save the data in an excell file
    #save_to_excel_company(scraper.data)

    # Converting the data to JSON format and saving it
    json_data = json.dumps(scraper.data, indent=4)
    with open('output/data.json', 'w') as json_file:
        json_file.write(json_data)

    print("Data has been written to data.json")

        
if __name__ == "__main__":
    main()
