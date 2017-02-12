# Using code borrowed from http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
# to force the browser to wait until the page has reloaded

from bs4 import BeautifulSoup
from splinter import Browser
import yaml
import pickle
import io
import os
import config
import time
import threading
from threading import Thread
import string

from dog import Dog

root_url = "http://www.fieldtrialdatabase.com/"
search_url = "dogSearch.php4"

max_dogs_displayed = 150

dog_limit = 20

scraping_threads = 2

def pause():
    time.sleep(0.1)

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_by_tag('html')

        # Keep an element until it is stale
        self.element_to_watch = self.old_page.first

    def page_has_loaded(self):
        new_page = self.browser.find_by_tag('html')
        try:
            if self.element_to_watch.checked:
                pass
            return False
        except:
            return True

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)

def get_dog_list(browser, search_query):
    """ Returns a list of dog name links from the given search query """

    # try:
    browser.fill("dogSearchText", search_query)
    pause()


    with wait_for_page_load(browser):
        browser.find_by_value("search").click()

    page = BeautifulSoup(browser.html, 'html.parser')
    # except:
        # print('WARNING: Recursing because of an exception')
        # return get_dog_list(browser, search_query)

    table = page.find_all(
            attrs={ "valign": "top"})[1]

    if table.tbody:
        return table.tbody.contents
    else:
        print ('Warning! No search results for query ' + search_query)
        return []

def extract_dog_set(browser, search_queries):
    browser.visit(root_url + search_url)
    time.sleep(2)

    with wait_for_page_load(browser):
        browser.find_option_by_text("Brittany").click()


    dog_set = set([]) # use a set to avoid duplicates

    for search_query in search_queries:
        new_dog_list = get_dog_list(browser, search_query)

        if len(new_dog_list) == max_dogs_displayed:
            print("Warning: a list is too large for full display")

        for dog in new_dog_list:
            # print(dog)
            dog_set.add(dog.a["href"])

    return dog_set


class SearchScraperThread(Thread):
    def __init__(self, search_query_subset):
        Thread.__init__(self)

        self._search_query_subset = search_query_subset

    def run(self):
        self._browser = Browser()
        self.output_dog_set = extract_dog_set(self._browser, self._search_query_subset)


def split_list(the_list, sections):
    # Split the given list into pieces
    elements_per_section = int(len(the_list) / sections)
    remainder = len(the_list) % sections

    out_sections = []

    for i in range(sections):
        subset = the_list[i * elements_per_section:
                        (i+1) * elements_per_section]
        if (i == sections - 1):
            remainder_subset = the_list[(i+1) * elements_per_section:
                                        (i+2) * elements_per_section + remainder]
            for element in remainder_subset:
                subset.append(element)

        out_sections.append(subset)

    return out_sections

def generate_dog_list(search_queries):
    big_dog_set = set([])

    threads = []
    subsections = split_list(search_queries, scraping_threads)

    for i in range(scraping_threads):
        new_thread = SearchScraperThread(subsections[i])
        new_thread.start()
        threads.append(new_thread)

    for i in range(scraping_threads):
        threads[i].join()

    for i in range(scraping_threads):
        output_set = threads[i].output_dog_set
        for dog in output_set:
            big_dog_set.add(dog)


    return list(big_dog_set)

def list_search_queries():
    """ Generate/extract the list of search queries that will be used to
    piece together a near-complete list of dogs """

    search_queries = []

    if config.limit_search():
        # search 2 common letters to probe for duplicates
        search_queries.append("a")
        search_queries.append("b")
    else:
       # search every combo of 2 letters to scrape all dogs
            for char1 in string.ascii_lowercase:
                search_queries.append(str(char1))
                # for char2 in string.ascii_lowercase:
                    # search_queries.append(str(char1) + str(char2))

    return search_queries



class DogScraperThread(Thread):
    def __init__(self, dog_list_subset):
        Thread.__init__(self)

        self._dog_list_subset = dog_list_subset

    def run(self):
        self._browser = Browser()
        self.output_dogs = []

        for dog_url in self._dog_list_subset:
            self._browser.visit(root_url + dog_url)
            dog = Dog.from_html(self._browser.html, dog_url)
            self.output_dogs.append(dog)

def extract_dog_stats(dog_list):
    if config.limit_search():
        dog_list = dog_list[0:dog_limit]

    dog_stats = []

    threads = []
    subsections = split_list(dog_list, scraping_threads)

    for i in range(scraping_threads):
        new_thread = DogScraperThread(subsections[i])
        new_thread.start()
        threads.append(new_thread)

    for i in range(scraping_threads):
        threads[i].join()

    for i in range(scraping_threads):
        for dog in threads[i].output_dogs:
            dog_stats.append(dog)

    yaml.dump(dog_stats, io.open("dog-stats.yaml", "w"))

    return dog_stats
