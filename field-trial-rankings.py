#! /usr/bin/env python3

from bs4 import BeautifulSoup
from splinter import Browser
import string

def get_dog_list(browser, search_query):
    browser.fill("dogSearchText", search_query)

    browser.find_option_by_text("Brittany").click()

    browser.find_by_value("search").click()

    page = BeautifulSoup(browser.html)

    table = page.find_all(
            attrs={ "valign": "top"})[1]

    if table.tbody:
        return table.tbody.contents
    else:
        return [ ]

if __name__ == "__main__":
    with Browser() as browser:
        browser.visit("http://www.fieldtrialdatabase.com/dogSearch.php4")

        search_queries = [ ]

        for char1 in string.ascii_lowercase:
            for char2 in string.ascii_lowercase:
                search_queries.append("" + char1 + char2)

        dog_list = [ ]

        for search_query in search_queries:
            list = get_dog_list(browser, search_query)

            if len(list) == 150:
                print("Warning: a list is too large for full display")

            for dog in list:
                if not dog_list.count(dog):
                    dog_list.append(dog)

        print(len(dog_list))
