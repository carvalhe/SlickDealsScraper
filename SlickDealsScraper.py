#### Switching branch name
from bs4 import BeautifulSoup
import requests
import re
# Config file information https://stackoverflow.com/questions/5055042/whats-the-best-practice-using-a-settings-file-in-python
import config

DEBUG = False

PREVIOUS_ITEMS = 'item_log.txt'


### Function is used to set up and crawl through slick deals, returning a list
def slick_crawler():
    #### Set up where you are requesting from
    # Add or remove items to search slick deals website for
    keyWords = ["switch", "PS4", "Xbox", "Gap", "Nintendo", "Twitch", "Camera", "Coffee"]
    # Add the user_input toe the google search url and request that
    domain = 'https://slickdeals.net/'
    source = requests.get(domain).text

    # create list to store url links
    deals = list()

    #### create soup from the page
    if(source is not None):
        soup = BeautifulSoup(source, 'lxml')
        #### Parse through the soup for the information you want
        # need the Div with a class of fpitem
        #for item in soup.find_all('div', class_= "fpitem  pctoff"):
        #item = soup.find_all("div", class_= "fpItem")
        for item in soup.find_all("div", class_= "fpItem"):
            if(DEBUG):
                print(item.prettify())
            #link = item[1].find("a", class_="itemTitle")
            # get the items title
            link = item.find("a", class_="itemTitle")

            # we now have the item title. we need to search it to check if it contains the keywords we are looking for
            if(link == None):
                continue
            # we have the link to an item, scan through its conents to see if it matches
            # with what we are searching for aka keyWords list
            for key in keyWords:
                if(key in link.text):
                    if(DEBUG):
                        print("Keyword match")
                    # print(item[1].find("a", class_= "viewDetailsBtn"))
                    urlDeal = item.find_all('a', href=True)
                    urlDeal = "https://slickdeals.net" + urlDeal[1]['href']
                    deals.append(urlDeal)
                    if(DEBUG):
                        print(urlDeal)
                    # break out so you dont add it twice
                    break
    return deals

### Function deletes duplicates from deals that are already seen before
def delete_dups(deals, previousPosts):
    # Open the previous items log for reading
    file_ = open(previousPosts, 'r')
    lines = file_.readlines()
    removed_deals = list()
    # return whats not in the file
    for item in deals:
        # add '\n' to the item name so that its the same as the txt file, or else
        # it is seen as a different string even if they look equal
        if(item + '\n' not in lines):
            removed_deals.append(item)
    file_.close()
    if(DEBUG):
        if(removed_deals == deals):
            print('no changes made')
        else:
            print('deleted some deals')
    return removed_deals

### Function that adds the new deals to the Slick deals log
def update_log(deals, previousPosts):
    # Open the file for writing, don't use 'w' as it may overwrite and insert at the start
    file_ = open(previousPosts, 'a+')
    for deal in deals:
        file_.write(deal)
        file_.write('\n')


### Function that posts this list of items to discord with webhooks
def post_discord(deals, url):
    # information on get/post requests https://www.geeksforgeeks.org/get-post-requests-using-python/
    # check if deals is empty, so you dont need to do anything
    if not deals:
        print('no deals to send to discord')
        return
    else:
        for deal in deals:
            r = requests.post(url, data={'content': deal})
    

def main():
    # Information on main, even on scripting in Python too
    # https://stackoverflow.com/questions/29652264/why-is-my-python-function-not-being-executed

    deals = slick_crawler()
    deals = delete_dups(deals, PREVIOUS_ITEMS)
    if(DEBUG):
        print(deals)
    update_log(deals, PREVIOUS_ITEMS)
    if(DEBUG):
        post_discord(deals, config.URL['TEST'])
    else:
        post_discord(deals, config.URL['IVAN'])



if __name__ == '__main__':
    main()