
# import packages 
from bs4 import BeautifulSoup
import urllib.request
import re


seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
release = []
opened = []          #we keep track of seen urls so that we don't revisit them
covid_pages = []

########## BASE CODE FROM CLASS ###############################################
maxNumUrl = 10; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
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

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        urls.append(childUrl)
        
        if seed_url in childUrl and childUrl not in seen:
            urls.append(childUrl)

###############################################################################
        

## Now check the webpages that we've collected for the word "COVID"
cutoff = 0 # initialize counter for the number of "COVID pages" found

for i in range(1, len(urls)):
    
    if cutoff < 20: # instructions say at least 10, so let's do 15 here 
        page = urls[i]
        req = urllib.request.Request(page,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(webpage)
        text = soup.get_text()
        
        all_words = text.split() 
        
        for i in range(len(all_words)):
            all_words[i] = re.sub('[\W\d]', '', all_words[i])
            all_words[i] = all_words[i].lower() 
        all_words = list(filter(None, all_words))
        
        print("Trying " + page)
        if "covid" in all_words:
            covid_pages.append(page)
            print("Covid mentoned.")
            cutoff += 1
        else:
            print("No covid mentions.")
                    

## Print the webpages that had COVID in them 
for i in covid_pages:
    print(i)
    
    