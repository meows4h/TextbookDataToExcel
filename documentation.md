# Documentation File
The goal of this file is to provide a higher level overview of how this script works to help identify issues, improvements, as well as future maintainability.

## At a Glance
If you're trying to modify the `Creating an Excel Sheet from Scratch`, modify `main.py` and subsequent functions used there.
If you're looking to change something in the other functions, you can find it in the `modes.py` script.
## main.py
This is what runs through the whole process. Initially it will ask the user what they wish to do, with most options passing the user off to the `modes.py` script. It also hosts the code for creating a new Excel sheet from scratch with the stored data.

Initially it will initialize with the configuration options and paths, as well as the data that it needs to import. The goal of this script is to incorperate all the relevant data for each book given from `bookstore.py`/`bookstore.csv` and combine it into `Book` objects from the `classes.py` script. After this is finalized, the list of `Book` objects are passed into an export function from `output.py`. Relevant data is pulled from various sources such as Outlook or Primo, using `grabber.py` and `analytics.py` respectively.
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
## modes.py
Aids in handling the various functions of the script, modularizing individual pieces into useful functions.
## output.py
This script has a single function: outputting an Excel sheet!
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