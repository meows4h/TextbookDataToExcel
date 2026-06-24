# Documentation File
The goal of this file is to provide a higher level overview of how this script works to help identify issues, improvements, as well as future maintainability.
## At a Glance
There are two primary methods that this script runs through: The CLI version and the GUI version. The CLI version is more or less function complete in how I intend for it to function and operate, though it still has some rough edges, especially in a user interaction factor. The GUI version is what will continue to receive updates and more improvements over time. These two versions can be toggled between in the `config.ini` file.
## main.py
This file serves as the starting point for the whole script. If the GUI mode is activated, it will start the GUI from `gui.py`, otherwise, it will take an input from the user and pass it over to `sheetmaker.py` if you're making a new sheet or to `modes.py` if you're using the other features.
## analytics.py
Anything related to handling data from Alma gets handled through this script. Between setting up the browser, parsing the HTML, and handling inputs for things such as the SQL.
## bookstore.py
Most of this code is pulled from the original bookstore data puller that was made to automate getting bookstore data. It will have the user pass a CAPTCHA and then have them select data to pull from to get the specific term of textbook data they are interested in.
## classes.py
Stores the frameworks and methods for interacting with storing and processing book related data.
## emails.py
Handles compiling and creating Excel sheets for PowerAutomate emails.
## enrollment.py
Handles pulling the relevant data from the enrollment csv file in order to get the maximum enrollment values.
## grabber.py
Deals with setting up and handling pulling data from the Outlook browser to get emails for individual professors.
## gui.py
This hosts all of the primary interactive GUI for the user.
## helpergui.py
This is a much slimmer and simpler version of the main GUI class, to be something much more modular and additive.
## modes.py
Aids in handling the various functions of the script, modularizing individual pieces into useful functions.
## output.py
This script has a single function: outputting an Excel sheet!
## sheetmaker.py
Performs all of the functions related to creating new sheets from scratch.
## utilties.py
This script hosts helpful functions that might be purposeful in multiple places around the various helper and main scripts. On top of this, it also helps to host hard coded data that is not necessary to keep in a configuration file (such as header values!). The organization is to help cut down on lines of code in other places, as well as keep information consistency so updating one variable does update it in all relevant places when needed.
## CSV Storage
In order to store all the data in a way that is accessible, quick, and aids in subsequent run times, all pulled data is compiled into `.csv` files, each with their own format. This makes it so we don't have to re-run the bookstore scraper, email grabber, or analytics scraper again every single time we wish to do something.
### analytics.csv
After parsing all the data from Alma, it is stored in this csv file to be used later.

Data is formatted as following:
ISBN, {'MMS Id': {'Types': [str], 'Copies': [int], 'Users': [int], 'CDL': [bool], 'Link': str}, ... }
### bookstore.csv
This data is all the raw information taken from the bookstore page, stored to be used later.

Data is formatted as following:
Term, Course Subject, Course Number, Section Number, Instructor, Title, Edition, Author, ISBN, Publisher, Requirement, SKU, Comments, Requisition Date
### emails.csv
Each time an instructor name is paired to an email, it is saved to this file to be used later.

Data is formatted as following:
Instructor Name, Email
### enrollment.csv
This is just a CORE report exported as a csv for all courses in the desired term. This must be done outside of the script itself.
## Config Files
### config.ini
Primary settings for the script, though some of these are redundant / only used by one half of the script.
### emails.ini
Holds all the template lines for emailing professors.
### headers.ini
Holds all the names of the headers as well as their relation to the internal variable name.