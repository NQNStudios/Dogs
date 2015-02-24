class Placements(object):
    """ Contains statistics about a dog's placements in a specific stake """

    def __init__(self):
        self.__total_count = 0
        self.__place_counts = { }

    @property
    def total_placements(self):
        return self.__total_count

    @property
    def place_counts(self):
        return self.__place_counts
    
    def num_placements(self, place):
        if place in self.__place_counts:
            return self.__place_counts[place]
        else:
            return 0

    def add_placement(self, place):
        self.__total_count += 1
        if place in self.__place_counts:
            self.__place_counts[place] += 1
        else:
            self.__place_counts[place] = 1

    def placement_percentage(self, place):
        return self.num_placements(place) / float(self.__total_count)
