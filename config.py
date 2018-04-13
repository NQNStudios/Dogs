import sys

bot_address = "nleroybot@gmail.com"

dogrc = open('.dogrc')
bot_password = dogrc.readline()


to_addresses = [
        "nelson.nleroy@gmail.com",
        "danwcampbell@gmail.com"
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

def use_saved_list():
    return sys.argv.count("--use-saved-list") != 0

def use_saved_stats():
    return sys.argv.count("--use-saved-stats") != 0

def limit_search():
    return sys.argv.count("--limit-search") != 0

def send_results():
    return sys.argv.count("--send-results") != 0
