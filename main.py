import sys
import configparser
from helpers.utilities import get_input, get_state
from helpers.modes import start_mode
from helpers.gui import start_app
from helpers.sheetmaker import make_excel_sheet

# SHORT TERM TODO:
# - MAIN INPUT FILE for emails, is supposed to be in MAIN not in HELPERS
# - Email Grabber state update: the refresh button just iterates again ! that is bad!
# - Adding the email language used for emails.py to the Options page

# MID TERM TODO:
# - Relook into fixing analytics data pulling
# - Ensure OneSearch scope is correct and/or reassess the bookstore ISBN pulling
# - Updating information properly, but also automatically

# BIG PICTURE TODO:
# - Adding prices from the bookstore site into the bookstore information!
# - Double check back over all the overdrive books among other ebook sources!
# - Finish GUI implementation (AND multithreading)
# - Finish README and Documentation
# - Improve scraping efficiency and looking up better methods ; Multiprocessing! ; Better SQL Queries
# - Safe guarding for error checking if extra time

# look at ISBN: 9781478647690 for verifying material type? 19 copies
# seems high
# this may have now been fixed due to onesearch checkign
# these were actually BNC books -- adding a location specifier to track which are ours!
# BNC copy number needs triple checking, seems to be wrong at a glance .
# check against this
# https://search.library.oregonstate.edu/permalink/01ALLIANCE_OSU/15hft48/cdi_proquest_ebookcentral_EBC6871151

config = configparser.ConfigParser()
config.read("config.ini")
main_cfg = config["Main"]
use_gui = get_state(main_cfg["gui"])

if use_gui:
    start_app()
else:
    print("Select mode:")
    input_text = """1. Create new Excel sheet (From Scratch w/ Cache)
    2. Update .csv files (Updating Script Cache)
    3. Create email Excel sheet (PowerAutomate)
    4. Update Excel sheet (Updating Sheet w/ Cache)
    Input: """
    mode_input = get_input(min=1, max=4, text=input_text)

    if mode_input != 1:
        start_mode(mode_input)
        sys.exit(1)  # quit out after alt use

    make_excel_sheet()
