#! /usr/bin/env python3

import os
import io
import pickle

import dog
from dog import Dog

import config
import site_tools
import email_tools
import rank_tools

if __name__ == "__main__":
    if os.path.isfile("dog-stats.pickle") and config.use_save:
        dog_stats = pickle.load(io.open("dog-stats.pickle", "rb"))
    else:
        dog_stats = site_tools.extract_dog_stats()

    for stake_type in dog.stake_types:
        for rank_method in rank_tools.rank_methods:
            rankings = rank_tools.rank(dog_stats, rank_method, stake_type)
            email_tools.send_rankings(rankings, rank_method, stake_type)
