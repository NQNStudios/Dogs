from bs4 import BeautifulSoup
from splinter import Browser
import string
import pickle
import io
import os
import config
import time

from dog import Dog

root_url = "http://www.fieldtrialdatabase.com/"
search_url = "dogSearch.php4"

max_dogs_displayed = 150

dog_limit = 20


def get_dog_list(browser, search_query):
    """ Returns a list of dog name links from the given search query """

    browser.fill("dogSearchText", search_query)
    browser.find_option_by_text("Brittany").click()
    browser.find_by_value("search").click()
    time.sleep(1)
    page = BeautifulSoup(browser.html, 'html.parser')

    table = page.find_all(
            attrs={ "valign": "top"})[1]

    if table.tbody:
        return table.tbody.contents
    else:
        return [ ]

def generate_dog_list(browser, search_queries):
    dog_set = set([]) # use a set to avoid duplicates

    for search_query in search_queries:
        time.sleep(1)
        new_dog_list = get_dog_list(browser, search_query)

        if len(new_dog_list) == max_dogs_displayed:
            print("Warning: a list is too large for full display")

        for dog in new_dog_list:
            dog_set.add(dog.a["href"])

    return list(dog_set)

def extract_dog_stats():
    with Browser('firefox') as browser:
        browser.visit(root_url + search_url)

        search_queries = [ ]

        if config.limit_search:
            # search 2 common letters to probe for duplicates
            search_queries.append("a")
            search_queries.append("b")
        else:
            # search every combo of 2 letters to scrape all dogs
            for char1 in string.ascii_lowercase:
                for char2 in string.ascii_lowercase:
                    search_queries.append(str(char1) + str(char2))

        # Don't scrape all those searches for the dog list if we have one
        # we can use already
        if os.path.isfile("dog-list.pickle") and config.use_saved_list:
            dog_list = pickle.load(io.open("dog-list.pickle", "rb"))
        else:
            dog_list = generate_dog_list(browser, search_queries)
            pickle.dump(dog_list, io.open("dog-list.pickle", "wb"))

        if config.limit_search:
            dog_list = dog_list[0:dog_limit]

        dog_stats = [ ]

        for dog_url in dog_list:
            browser.visit(root_url + dog_url)
            dog = Dog.from_html(browser.html, dog_url)
            dog_stats.append(dog)

        pickle.dump(dog_stats, io.open("dog-stats.pickle", "wb"))

        return dog_stats
