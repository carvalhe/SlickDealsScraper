#### Switching branch name
from bs4 import BeautifulSoup
import requests
import csv
import re

DEBUG = True

#### Set up where you are requesting from
keyWords = ["Switch", "Steel"]
# Add the user_input toe the google search url and request that
domain = 'https://slickdeals.net/'
source = requests.get(domain).text

#### Create a csv file to store information later
# do a w for write
csv_file = open('slickdeals_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)



#### create soup from the page
if(source is not None):
    soup = BeautifulSoup(source, 'lxml')
    #### Parse through the soup for the information you want
    # need the Div with a class of fpitem
    #for item in soup.find_all('div', class_= "fpitem  pctoff"):
    item = soup.find_all("div", class_= "fpItem")
    if(DEBUG):
        print(item[1].prettify())
    #link = item[1].find("a", class_="itemTitle")
    # we now have the item title. we need to search it to check if it contains the keywords we are looking for
    link = item[1].find("a", class_="itemTitle")
    if(DEBUG):
        print(link.text)
    # we have the link to an item, scan through its conents to see if it matches
    # with what we are searching for aka keyWords list
    for key in keyWords:
        if(key in link.text):
            print("true")
csv_file.close()
