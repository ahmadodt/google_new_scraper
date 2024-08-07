# google_new_scraper
This is a simple task to scrape google news and some other websites to search for equity checks, how much  megawats investments and if the investors are investing in solar farms

This was written for the follwoing task:
 Your goal is to find news articles or webpages that contain the target information about the given company. Two cases (choose whichever):

(1) We want to find information on solarpark investors, namely the size of the equity checks they are writing, the megawatts of the solarparks they are investing in, and in general whether they are investing in solarparks (because you are likely to find some renewable energy investors not explictly investing in solarparks).

Companies: ENVIRIA Energy Holding GmbH, ENREGO Energy GmbH, HIH Invest Real Estate Austria GmbH, Merkle Germany GmbH.

And here's how i tackled it:

first i tried searching for good websites to get information about the companies
I tried Bloomberg as it is a financial related website but the first of our companies ENVIRIA have no search results there so it was rejected.
Then I checked the blogs in each of the companies websites and it was a bit succesful as i only tried for ENVIRIA but i noticed that the data I'm getting does'nt include the data i want. A lot of them are like advice and ads for the company. **(this is scraping_v1.py)**

Therefore this lead me to Google news and here I found the info I need.

Therefore I learned how to scrap Google news.
Here I had access to the html text inside all the news articles that the name of the company as a search got me.
So i tried extracting  the important details we want from those text:
I had two option the first would be to ry without any LLM models threfore,
  I tried Regex which lead to a lot of info slipping by and not being captured.
  Then I tried looking through entities using spacy library. This made capturing the money or megawats easier. But still it had only words as a result.
  After that I extracted sentences where there is a match to the invest_keywords in its stemmatized form.This lead to me having access to the sentences containing investig keywords and money entity
  yet from those sentences it is hard to understand and point which investment go into solarfarms and which not. And which belongs to which company.
  Therefore I came back to the idea and used an LLM. basically i we scrap google news and if the name of the company is present in the text i would iinput the text and my prompt into the model for it to give me a better result. The prompt take into account which company is present in the article to reduce the models chance to halucinate.
  An even better aproach would be to ues RAG models which could enhance the extraction of the data in the news articles chosen
  This was not experimented much with as i need a better hardware for this task.

**CODE**
scraping_v2.py is the main and the one you need to check.
scraping_v1.py in old folder is the one i used for checking the blogsin ENVIRIA site
LLM.py contain the code  for running the LLM function 
scraping_basic.py contains small basic functions from beautifulsoup and requests


**RUN**
conda env create -f environment.yaml
conda activate web_scraping_env
python scraping_v2.py
