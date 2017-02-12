bot_address = "nleroybot@gmail.com"

dogrc = open('.dogrc')
bot_password = dogrc.readline()


to_addresses = [
        "nelson.nleroy@gmail.com",
        "daniel.campbell@slcschools.org"
        ]

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

use_saved_list = True
use_saved_stats = True
limit_search = False
send_results = True
