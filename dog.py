from bs4 import BeautifulSoup

from placements import Placements
import config

#stake_types = [ 'AA', 'GD' ]
stake_types = config.stake_types

class Dog(object):
    """ Contains useful information about a dog """

    def __init__(self, url):
        self.__url = url
        self.__name = ""
        self.__placements = { }

        for stake_type in stake_types:
            self.__placements[stake_type] = Placements()

    @property
    def url(self):
        return self.__url

    @property
    def name(self):
        return self.__name

    @property
    def placements(self):
        return self.__placements

    @staticmethod
    def from_html(html, url):
        print (url)
        print (html)
        dog = Dog(url)

        page = BeautifulSoup(html, 'html.parser')

        # name the dog
        dog.__name = page.title.text.strip()
        print (dog.__name)

        # search the placements table for placement stats
        print (page.body.prettify())
        placements_table = page.body.find_all('table', border="1", cellpadding="2")[0]
        rows = placements_table.tbody.contents[1:]

        # for each stake type we're interested in, tally the number of
        # placements for each different place number
        for stake_type in stake_types:
            for row in rows:
                stake = row.contents[2].text.strip()
                place = int(row.contents[3].text.strip())

                if stake.count(stake_type):
                    dog.placements[stake_type].add_placement(place)

        return dog
