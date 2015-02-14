#! /usr/bin/env python3

from bs4 import BeautifulSoup
from splinter import Browser
import string
import re

root_url = "http://www.fieldtrialdatabase.com/"

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

def process_dog(browser, dog_url):
    browser.visit(root_url + dog_url)

    page = BeautifulSoup(browser.html)

    placements_text = page.findAll('b', text = re.compile("[0-9]+ PLACEMENTS"))
    num_placements_str = placements_text[0].text.strip()

    num_placements = int(num_placements_str[0:num_placements_str.find(" ")])

    placements_table = page.findAll('table', border="1", cellpadding="2")[0]
    rows = placements_table.tbody.contents[1:]

    num_first_place = 0

    for row in rows:
        place = int(row.contents[3].text.strip())
        if place == 1:
            num_first_place = num_first_place + 1

    place_dog(dog_url, num_placements, num_first_place / float(num_placements))

dog_rankings = 10

most_placing_dogs = [ ]
best_placing_dogs = [ ]

def place_dog(dog_url, num_placements, percent_first):
    index = len(most_placing_dogs)

    while index > 0 and num_placements > most_placing_dogs[index - 1][1]:
        index = index - 1

    if index < 10:
        most_placing_dogs.insert(index, ( dog_url, num_placements ))
        if len(most_placing_dogs) > 10:
            most_placing_dogs.pop(10)

    if num_placements < 3:
        return # we don't want to let minimally placing dogs compete on this front

    index = len(best_placing_dogs)

    while index > 0 and percent_first > best_placing_dogs[index - 1][1]:
        index = index - 1

    if index < 10:
        best_placing_dogs.insert(index, ( dog_url, percent_first ))
        if len(best_placing_dogs) > 10:
            best_placing_dogs.pop(10)

if __name__ == "__main__":
    with Browser() as browser:
        browser.visit(root_url + "dogSearch.php4")

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

        for dog in dog_list[0:25]:
            process_dog(browser, dog.a["href"])

        print(most_placing_dogs)
        print(best_placing_dogs)
