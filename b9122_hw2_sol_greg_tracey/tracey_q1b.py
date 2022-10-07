

# import packages 
from bs4 import BeautifulSoup
import urllib.request
import re

seed_url = "https://www.sec.gov/news/pressreleases"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
release = []
opened = []          #we keep track of seen urls so that we don't revisit them
charges_pages = []
full_text = []

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
    soup = BeautifulSoup(webpage, features="lxml")  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('td',{'class':'views-field views-field-field-display-title'}):
        tag = tag.find('a')
        childUrl = tag['href'] #extract just the link
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        urls.append(childUrl)


cut = 0

for i in range(1, len(urls)):
    
    if cut < 21:
        page = urls[i]
        req = urllib.request.Request(page, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(webpage, features = 'lxml')
        text = soup.get_text()
        
        all_words = text.split() 
        
        for i in range(len(all_words)):
            all_words[i] = re.sub('[\W\d]', '', all_words[i])
            all_words[i] = all_words[i].lower() 
        all_words = list(filter(None, all_words))
        
        all_words = all_words[:len(all_words) - 30] # get rid of random hyperlinks at the bottom
        output_text = ' '.join(all_words)
        
        if "charges" in all_words:
            print(page)
            print("Charges.")
            charges_pages.append(page)
            full_text.append(output_text)
            cut += 1
        else:
            print(page)
            print("No charges.")
            
for i in range(1, len(charges_pages)):
    print(charges_pages[i]) 
    print(" ")
    print(full_text[i])
    print(" ")


