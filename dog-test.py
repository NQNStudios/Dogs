#! /usr/bin/env python3

from dog import Dog
from splinter import Browser

if __name__ == "__main__":
    with Browser() as browser:
        browser.visit("http://www.fieldtrialdatabase.com/dog.php4?id=4066")
        dog = Dog.from_html(browser.html)

        print(dog.name)
        print(dog.placements["AA"].num_placements(0))
        print(dog.placements["AA"].num_placements(3))
        print(dog.placements["AA"].placement_percentage(3))

