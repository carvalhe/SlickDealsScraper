#### Switching branch name
from bs4 import BeautifulSoup
import requests
import csv

DEBUG = False

#### Set up where you are requesting from
keyWords = "laptop"
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
    print("hello")
    #### Parse through the soup for the information you want
    # need the Div with a class of fpitem
    #for item in soup.find_all('div', class_= "fpitem  pctoff"):
    item = soup.find_all("div", class_= "fpItem")
    print(item[1])

csv_file.close()
