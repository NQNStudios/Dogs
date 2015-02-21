#! /usr/bin/env python3

import dog
from dog import Dog

import site-tools
import email-tools
import rank-tools

dog_rankings = 25
min_placements = 25

most_placing_dogs = [ ]
best_placing_dogs = [ ]
all_dogs = [ ]

def place_dog(dog_url, num_placements, percent_first):
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


if __name__ == "__main__":
    dog_stats = site-tools.extract_dog_stats()

    for stake_type in stake_types:
        for rank_method in rank_methods:
            rankings = get_rankings(dog_stats, rank_method)
t
            email-tools.send_rankings(rankings, rank_method)
