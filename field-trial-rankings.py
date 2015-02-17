#! /usr/bin/env python3

from bs4 import BeautifulSoup
from splinter import Browser
import string
import re
import pickle
import os.path
import io

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
    if len(placements_text) == 0: # avoid a weird error?
        return

    num_placements_str = placements_text[0].text.strip()

    num_placements = int(num_placements_str[0:num_placements_str.find(" ")])

    placements_table = page.findAll('table', border="1", cellpadding="2")[0]
    rows = placements_table.tbody.contents[1:]

    num_first_place = 0

    for row in rows:
        place = int(row.contents[3].text.strip())
        if place == 1:
            num_first_place = num_first_place + 1

    percent = 0
    if num_placements > 0:
        percent = num_first_place / float(num_placements) 

    place_dog(dog_url, num_placements, percent)

dog_rankings = 10
min_placements = 10

most_placing_dogs = [ ]
best_placing_dogs = [ ]
all_dogs = [ ]

dog_stats_saved = False

def place_dog(dog_url, num_placements, percent_first):
    if not dog_stats_saved:
        all_dogs.append(( dog_url, num_placements, percent_first ))
    
    # rank by number of placements
    index = len(most_placing_dogs)

    while index > 0 and num_placements > most_placing_dogs[index - 1][1]:
        index = index - 1

    if index < dog_rankings:
        most_placing_dogs.insert(index, ( dog_url, num_placements ))
        if len(most_placing_dogs) > dog_rankings:
            most_placing_dogs.pop(dog_rankings)

    if num_placements < min_placements:
        return # we don't want to let minimally placing dogs compete on this front

    index = len(best_placing_dogs)

    while index > 0 and percent_first > best_placing_dogs[index - 1][1]:
        index = index - 1

    if index < dog_rankings:
        best_placing_dogs.insert(index, ( dog_url, percent_first ))
        if len(best_placing_dogs) > dog_rankings:
            best_placing_dogs.pop(dog_rankings)

def generate_dog_list(search_queries):
    dog_set = set([]) # use a set to avoid duplicates

    for search_query in search_queries:
        new_dog_list = get_dog_list(browser, search_query)

        if len(new_dog_list) == 150:
            print("Warning: a list is too large for full display")

        for dog in new_dog_list:
            dog_set.add(dog.a["href"])

    return list(dog_set)

limit_search = False
start_over = False

dog_limit = 40

if __name__ == "__main__":
    if os.path.exists("dog-stats.pickle") and not start_over:
        dog_stats_saved = True

        all_dogs = pickle.load(io.open("dog-stats.pickle", "rb"))

        for dog in all_dogs:
            place_dog(dog[0], dog[1], dog[2])
    else:
        with Browser() as browser:
            browser.visit(root_url + "dogSearch.php4")

            search_queries = [ ]

            if limit_search:
                search_queries.append("a")
                search_queries.append("b")
            else:
                for char1 in string.ascii_lowercase:
                    for char2 in string.ascii_lowercase:
                        search_queries.append("" + char1 + char2)
            
            dog_list = [ ]

            if os.path.exists("dog-list.pickle") and not start_over:
                dog_list = pickle.load(io.open("dog-list.pickle", "rb"))
            else:
                dog_list = generate_dog_list(search_queries)
                pickle.dump(dog_list, io.open("dog-list.pickle", "wb"))

            if limit_search:
                dog_list = dog_list[0:dog_limit]

            for dog in dog_list:
                process_dog(browser, dog)

            pickle.dump(all_dogs, io.open("dog-stats.pickle", "wb"))

    print(most_placing_dogs)
    print(best_placing_dogs)
