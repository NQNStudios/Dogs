from bs4 import BeautifulSoup
from splinter import Browser
import yaml
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

def pause():
    time.sleep(0.1)

def get_dog_list(browser, search_query):
    """ Returns a list of dog name links from the given search query """

    try:
        browser.fill("dogSearchText", search_query)
        pause()
        browser.find_option_by_text("Brittany").click()

        pause()
        pause()

        browser.find_by_value("search").click()
        pause()

        page = BeautifulSoup(browser.html, 'html.parser')
    except:
        print('WARNING: Recursing because of an exception')
        return get_dog_list(browser, search_query)

    table = page.find_all(
            attrs={ "valign": "top"})[1]

    if table.tbody:
        return table.tbody.contents
    else:
        return [ ]

def generate_dog_list(browser, search_queries):
    # TODO split search_queries into segments and multi-thread this
    # (will require multiple browsers)
    browser.visit(root_url + search_url)
    time.sleep(5)

    dog_set = set([]) # use a set to avoid duplicates

    for search_query in search_queries:
        new_dog_list = get_dog_list(browser, search_query)

        if len(new_dog_list) == max_dogs_displayed:
            print("Warning: a list is too large for full display")

        for dog in new_dog_list:
            dog_set.add(dog.a["href"])

    return list(dog_set)



def list_search_queries():
    """ Generate/extract the list of search queries that will be used to
    piece together a near-complete list of dogs """

    search_queries = []

    if config.limit_search():
        # search 2 common letters to probe for duplicates
        search_queries.append("a")
        search_queries.append("b")
    else:
        with open('searches.txt', 'r') as searches:
            search_queries = searches.readlines()

    return search_queries


def extract_dog_stats():
    with Browser('firefox') as browser:

        # Don't scrape all those searches for the dog list if we have one
        # we can use already
        if os.path.isfile("dog-list.yaml") and config.use_saved_list():
            dog_list = yaml.load(io.open("dog-list.yaml", "r"))
        else:
            dog_list = generate_dog_list(browser, search_queries)
            yaml.dump(dog_list, io.open("dog-list.yaml", "w"))

        if config.limit_search():
            dog_list = dog_list[0:dog_limit]

        print('Dogs in list:' + str(len(dog_list)))

        dog_stats = [ ]

        for dog_url in dog_list:
            browser.visit(root_url + dog_url)
            dog = Dog.from_html(browser.html, dog_url)
            dog_stats.append(dog)

        pickle.dump(dog_stats, io.open("dog-stats.pickle", "wb"))

        return dog_stats
