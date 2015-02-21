from dog import Dog

class RankingMethod(object):
    def __init__(self, name, qualifier, comparator, formatter):
        self.name = name
        self.qualifies = qualifier
        self.compare = comparator
        self.format = formatter

def rank(dog_stats, rank_method):
    rankings = [ ]

    for dog in dog_stats:

        # make sure the dog qualifies in this ranking
        if not rank_method.qualifies(dog):
            continue

        # starting from last place, move the next dog up the line until it
        # loses
        index = len(rankings)
        while index > 0 and rank_method.compare(dog, rankings[index - 1]):
            index -= 1

        # if it's won a place in the rankings, add it
        if index < dog_rankings:
            rankings.insert(index, dog)

            # if there are too many now, bump the last one off
            if (len(rankings) > dog_rankings):
                rankings.pop(dog_rankings)

    return rankings

dog_rankings = 25
min_placements = 25

rankmethods = [ ]

def most_placements_qualifier():
    return true

def most_placements_compare():


most_placements = RankingMethod("Most Placements Dog Rankings",
        most_placements_qualifier, most_placements_compare, most_placements_format)
