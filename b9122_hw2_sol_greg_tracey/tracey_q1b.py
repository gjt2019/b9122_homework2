
# Greg Tracey
# 10 October 2022
# B9122: Computing for Business Research
# Homework #2
###############################################################################

# import packages 
from bs4 import BeautifulSoup
import urllib.request
import re

# pass seed URL of SEC press release site
seed_url = "https://www.sec.gov/news/pressreleases"

# lists for keeping track of webpages
urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
charges_pages = []
full_text = []

cutoff = 20 # set number of press releases wanted to 20

########## BASE CODE FOR VISITING SITES FROM CLASS ############################
print("Starting with url="+str(urls))
while len(urls) > 0 and len(charges_pages) < cutoff:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below
###############################################################################

    soup = BeautifulSoup(webpage, features="lxml")  
    
    # only check for charges mention if page has not already been marked
    if curr_url not in charges_pages:
    
        # Get text from webpages and split it up into a list of words
        text = soup.get_text()
        all_words = text.split() 
        
        # clean up list of words
        for i in range(len(all_words)):
            all_words[i] = re.sub('[\W\d]', '', all_words[i])
            all_words[i] = all_words[i].lower() 
        all_words = list(filter(None, all_words))
        
        all_words = all_words[:len(all_words) - 30] # get rid of random hyperlinks at the bottom
        output_text = ' '.join(all_words)
        
        # Check pages for a mention of "charges" and report if one is found
        if "charges" in all_words:
            print("Charges.")
            charges_pages.append(curr_url)
            full_text.append(output_text)
        else:
            print("No charges.")


    # Put child URLs into the stack
    for tag in soup.find_all('td',{'class':'views-field views-field-field-display-title'}):
        tag = tag.find('a')
        childUrl = tag['href'] #extract just the link
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        urls.append(childUrl)
        
    if seed_url in childUrl and childUrl not in seen:
        seen.append(childUrl)
        
    
# Print out URLS and text of press releases 
for i in range(1, len(charges_pages)):
    print(charges_pages[i]) 
    print("/n" + full_text[i] + "\n")



