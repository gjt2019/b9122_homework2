
# Greg Tracey
# 10 October 2022
# B9122: Computing for Business Research
# Homework #2
###############################################################################

# import packages 
from bs4 import BeautifulSoup
import urllib.request
import re

# pass seed URL of Federal Reserve press release site
seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"

# lists for keeping track of webpages
urls = [seed_url]    # queue of urls to crawl
seen = [seed_url]    # stack of urls seen so far
opened = []          # keep track of seen urls so that we don't revisit them
covid_pages = []

cutoff = 15 # initialize counter for the number of "COVID pages" found

########## BASE CODE FOR VISITING SITES FROM CLASS ############################
print("Starting with url="+str(urls))
while len(urls) > 0 and len(covid_pages) < cutoff:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= " + curr_url)
        print(ex)
        continue    #skip code below
###############################################################################

    soup = BeautifulSoup(webpage, features="lxml")  
    
    # only check for COVID mention if page has not already been marked
    if curr_url not in covid_pages:
        
        # Get text from webpages and split it up into a list of words
        text = soup.get_text()
        all_words = text.split() 
        
        # clean up list of words
        for i in range(len(all_words)):
            all_words[i] = re.sub('[\W\d]', '', all_words[i])
            all_words[i] = all_words[i].lower() 
        all_words = list(filter(None, all_words))
        
        # Check pages for a mention of COVID and report if one is found
        if "covid" in all_words:
            covid_pages.append(curr_url)
            print("Covid mentioned.")
        else:
            print("No mention.")
        
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        urls.append(childUrl)
        
        if seed_url in childUrl and childUrl not in seen:
            seen.append(childUrl)

## Print the webpages that had COVID in them 
print("This is a list of webpages that contained the word COVID:")
for i in covid_pages:
    print(i)
    
    