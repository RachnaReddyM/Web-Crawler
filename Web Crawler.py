from bs4 import BeautifulSoup
import requests
import re
import sys
import time


# check_visited function is used to check if the URL is visited
# returns True if visited before, else False

def check_visted(url):
    global visited
    for vurl in visited:
        if(url == vurl):
            return True
    return False


listurl = [] # a list used to hold the currently crawled URLs 
visited = [] # a list used to hold the visited URLs
seedurl = "https://en.wikipedia.org/wiki/Tropical_cyclone" # a string consists of the seed URL
listurl.append(seedurl)
visited.append(seedurl)
depth = 1
no_of_url_at_current = 1
no_of_url_at_next = 0
file1 = open("Task 1-E",'w+') # open file to write the crawled URLS


while(depth < 6):
    current_url = listurl.pop(0)
    time.sleep(1) # a delay of atleast one second in implemented between HTTP requests
    handle = requests.get(current_url)
    no_of_url_at_current = no_of_url_at_current - 1

    html_raw_data =  handle.text
    soup = BeautifulSoup(html_raw_data, 'html.parser')

    # Get only Body text from Page, ignoring References, right navigation and URLS below images
    if len(soup.find('ol', attrs={'class': 'references'}) or ()) > 1:
        soup.find('ol', attrs={'class': 'references'}).decompose()
    if len(soup.find('div', attrs={'class': 'thumb tright'}) or ()) > 1:
        soup.find('div', attrs={'class': 'thumb tright'}).decompose()
    if len(soup.find('div', attrs={'id': 'toc'}) or ()) > 1:
        soup.find('div', attrs={'id': 'toc'}).decompose()
    if len(soup.find('table', attrs={'class': 'vertical-navbox nowraplinks'}) or ()) > 1:
        soup.find('table', attrs={'class': 'vertical-navbox nowraplinks'}).decompose()
    if len(soup.find('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}) or ()) > 1:
        soup.find('table', attrs={'class': 'vertical-navbox nowraplinks hlist'}).decompose()

    data = soup.find('div', attrs={'id': 'mw-content-text'})
    for urls in data.find_all('a', attrs={'href': re.compile("^/wiki")}):
        if ':' not in urls.get('href'):  #to exclude the administrative URLs
            final = "https://en.wikipedia.org" + urls.get('href')
            str1= final.split('#')[0]
            if(not check_visted(str1)): # to check if URL is visited
                listurl.append(str1)
                if (len(visited) < 1000): # to check if the count of URLs crawled is less than 1000
                    visited.append(str1)
                else:
                    for i,val in enumerate(visited):
                        file1.write(str(i+1) + ". " + str(val) + "\n") #write each URL to file
                    file1.close()
                    sys.exit(0)
                no_of_url_at_next = no_of_url_at_next +1
		
		
    if(no_of_url_at_current == 0):
        depth =depth +1               # depth is incremented when all nodes are crawled
        no_of_url_at_current = no_of_url_at_next
        no_of_url_at_next = 0

    	
	

for i,val in enumerate(visited):
    file1.write(str(i+1) + ". " + str(val) + "\n") #write each URL to file
	

file1.close() # file close at the end
