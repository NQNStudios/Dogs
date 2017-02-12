#! /usr/bin/env python3

import os
import io
import pickle
from splinter import Browser
import yaml

import dog

import config
import site_tools
import email_tools
import rank_tools


def compare_list_with_old(current_list, old_list_path):
    """ Print an overlap comparison of the two given lists """
    old_list = pickle.load(open(old_list_path, 'rb'))

    print("Number of dogs found by old search method: " + str(len(old_list)))
    print("Number of dogs found by new search method: " + str(len(current_list)))

    dogs_not_in_new = []

    # for dog in old_list:
        # if current_list.count(dog) == 0:
            # dogs_not_in_new.append(dog)
            # print('Dog missed by new search method: ' + dog)



if __name__ == "__main__":
    # Extract a dog list using the search queries in the text file
    search_queries = site_tools.list_search_queries()

    # Don't scrape all those searches for the dog list if we have one
    # we can use already
    if os.path.isfile("dog-list.yaml") and config.use_saved_list():
        dog_list = yaml.load(io.open("dog-list.yaml", "r"))
    else:
        dog_list = site_tools.generate_dog_list(search_queries)
        yaml.dump(dog_list, io.open("dog-list.yaml", "w"))

    # Compare the new list with the old one
    compare_list_with_old(dog_list, "previous_stats/dog-list.pickle")

    # don't bother extracting all the dog stats if we have a save
    if os.path.isfile("dog-stats.yaml") and config.use_saved_stats():
        dog_stats = pickle.load(io.open("dog-stats.yaml", "r"))
    else:
        dog_stats = site_tools.extract_dog_stats(dog_list)
        yaml.dump(dog_stats, io.open("dog-stats.yaml", "w"))

    for stake_type in dog.stake_types:
        for rank_method in rank_tools.rank_methods:
            rankings = rank_tools.rank(dog_stats, rank_method, stake_type)
            if config.send_results():
                email_tools.send_rankings(rankings, rank_method, stake_type)
            else:
                print(rankings)
                pass
