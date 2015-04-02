from dog import Dog

import config

dog_rankings = 25

class RankingMethod(object):
    def __init__(self, name, qualifier, comparator, formatter):
        self.name = name
        self.qualifies = qualifier
        self.compare = comparator
        self.format = formatter

def rank(dog_stats, rank_method, stake_type):
    rankings = [ ]

    for dog in dog_stats:

        # make sure the dog qualifies in this ranking
        if not rank_method.qualifies(dog, stake_type):
            continue

        # starting from last place, move the next dog up the line until it
        # loses
        index = len(rankings)
        while index > 0 and rank_method.compare(dog, rankings[index - 1], stake_type):
            index -= 1

        # if it's won a place in the rankings, add it
        if index < dog_rankings:
            rankings.insert(index, dog)

            # if there are too many now, bump the last one off
            if (len(rankings) > dog_rankings):
                rankings.pop(dog_rankings)

    return rankings

rank_methods = [ ]

def most_placements_qualifier(dog, stake_type):
    return True

def most_placements_compare(dogA, dogB, stake_type):
    return dogA.placements[stake_type].total_placements > \
            dogB.placements[stake_type].total_placements

def most_placements_format(dog, stake_type):
    return dog.name + " (" + str(dog.placements[stake_type].total_placements) + " placements)"

most_placements = RankingMethod("Most Placements Dog Rankings",
        most_placements_qualifier, most_placements_compare, most_placements_format)

rank_methods.append(most_placements)

def best_record_qualifier(dog, stake_type):
    min_placements = config.stake_qualifiers[stake_type]
    return dog.placements[stake_type].total_placements > min_placements

def best_record_compare(dogA, dogB, stake_type):
    return dogA.placements[stake_type].placement_percentage(1) > \
            dogB.placements[stake_type].placement_percentage(1)

def best_record_format(dog, stake_type):
    return dog.name + " (" \
            + "{0:.1f}".format(100 * dog.placements[stake_type].placement_percentage(1)) \
            + "% first place)"

best_record = RankingMethod("Best Placement Record Dog Rankings",
        best_record_qualifier, best_record_compare, best_record_format)

rank_methods.append(best_record)

def best_average_qualifier(dog, stake_type):
    min_placements = config.stake_qualifiers[stake_type]
    return dog.placements[stake_type].total_placements > min_placements

def average_placement(dog, stake_type):
    sum = 0

    for place in range(1, config.last_place + 1):
        count = dog.placements[stake_type].num_placements(place)
        sum += place * count

    return sum / float(dog.placements[stake_type].total_placements)

def best_average_compare(dogA, dogB, stake_type):
    return average_placement(dogA, stake_type) < average_placement(dogB, stake_type)

def best_average_format(dog, stake_type):
    return dog.name + " (" \
            + "{0:.2f}".format(average_placement(dog, stake_type)) \
            + " average)"

best_average = RankingMethod("Best Placement Average Dog Rankings",
        best_average_qualifier, best_average_compare, best_average_format)

rank_methods.append(best_average)
