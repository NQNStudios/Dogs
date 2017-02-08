bot_address = "nleroybot@gmail.com"

emailrc = open('.emailrc')
bot_password = emailrc.readline()

to_addresses = [
        "nelson.nleroy@gmail.com",
        "daniel.campbell@slcschools.org"
        ]

use_save = True

last_place = 4

stake_types = [ 'AA', 'OAA', 'AAA', 'GD', 'OGD', 'AGD' ]
stake_qualifiers = {
    'AA': 25,
    'OAA': 10,
    'AAA': 10,
    'GD': 25,
    'OGD': 20,
    'AGD': 15
}

limit_search = True
