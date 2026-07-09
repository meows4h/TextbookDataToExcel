# Documentation File
The goal of this file is to provide a higher level overview of how this script works to help identify issues, improvements, as well as future maintainability.
## At a Glance
There are two primary methods that this script runs through: The CLI version and the GUI version. The CLI version is more or less function complete in how I intend for it to function and operate, though it still has some rough edges, especially in a user interaction factor. The GUI version is what will continue to receive updates and more improvements over time. These two versions can be toggled between in the `config.ini` file.
---
## main.py
This file serves as the starting point for the whole script. If the GUI mode is activated, it will start the GUI from `gui.py`, otherwise, it will take an input from the user and pass it over to `sheetmaker.py` if you're making a new sheet or to `modes.py` if you're using the other features.
## analytics.py
Anything related to handling data from Alma gets handled through this script. Between setting up the browser, parsing the HTML, and handling inputs for things such as the SQL.
### get_columns
This function is where all the information related to generating SQL templates is stored. I found it much easier to track things in lists of dictionaries, with each dictionary containing a "Key" value for the section of the database it is searching, as well as "Cols" or columns which stores a list of the values that are listed under the associated "Key" value. Giving this function different values while calling returns different templates for different purposes. Due to how some listings do not appear while some columns are present, some of these are broken up into really small pieces.
### get_col_len
Returns the total number of columns within the SQL template. This helps with tracking how many columns need to be searched across while reading the tables within Alma analytics.
### get_table
Handles reading and parsing out the table information from the Alma screen.
### pull_one_search
Takes a list of MMS IDs and returns a list of the same size of `True` or `False`. False indicates that NO OneSearch listings appeared under the MMS ID search, while True indicates that something did return. This aids in finding out which MMS IDs and listings are still in circulation.
### pull_data
Given some data, this function automates creating a SQL statement and pulling data from the database.
### input_sql
Automates opening the SQL input window in Alma and inputting the given text.
### check_element
Aids in automating checking whether a given HTML element is present on the page, to know when it is okay to move to the next step.
### click_element
A template for telling the web driver what to click given some details about the specific HTML element.
### process_new_isbn
UNFINISHED and UNUSED; This function would ideally be used to find what ISBNs we do own for particular books from the bookstore, where a different ISBN is provided.
### process_analytics
Function that interacts with the other scripts to aid in pulling the analytics data given the web driver. Contains all the logic for how to process each set of information.
### setup_analytics
Creates and sets up the web browser to be prepared for automation tasks.
### setup_sql
Given a set of keys and columns to read, creates a complete SQL statement to use.
### export_analytics
Exports the data to a given csv file path.
### import_analytics
Imports the data from the given csv file path.

## bookstore.py
Most of this code is pulled from the original bookstore data puller that was made to automate getting bookstore data. It will have the user pass a CAPTCHA and then have them select data to pull from to get the specific term of textbook data they are interested in.
### str_clean
Removes certain special characters and whitespace from strings, aids in standardizing book titles.
### get_page_soup
Uses the BS4 library to grab a given URL, take the HTML contents and turn it into a workable form of data.
### get_link
Helper function to reduce number of replace statements later, simply helps create a link to use for price comparisons.
### get_prices
UNFINISHED and UNUSED; If there were to be a cost analysis function, this is what it would be, but the volume of books makes it a little too difficult to query this webserver as much as we would like to so it remains commented out.
### pull_textbook_data
The master information pulling function for the bookstore data.
### pull_info
Imports data from the bookstore csv file, mainly used by other parts of the program.

## classes.py
Stores the frameworks and methods for interacting with storing and processing book related data.
### Book (Class)
- Contstructor
Creating an object requires a dictionary of a couple different values: Related course, section, instructor name and email, enrollment information, the ISBN, book title, author, edition, publisher, requirements state, requisition date, the bookstore comment, and the Alma Analytics data for the given book. The constructor will parse out the information to make it more easily accessible for processing later.
- add_course
When another entry for a book is found that already exists as an object, the new course information gets added via this function.
- add_section
Similar to the course entry, but instead adding a section to an existing course within an existing book.
- add_isbn
Adding ISBN values for different variants of the same book.
- add_enroll
Putting in additional enrollment information into the book to track all the campuses and possible enrollment values.
- add_required
If at any point a bookstore listing has the book as "Required", it sets the book to that status using this function.
### get_max_index
Finds the index of the course with the most sections within it in order to aid in reducing column count, as well as ensuring the largest courses are always first (leftmost).
### get_max_courses
Gets the total number of course sections to have (the number of courses the book with the most courses has).
### get_max_sections_list
Finds the number of sections needed for each course section. As an example, if we have two books, one book has 3 course with 10, 5, and 3 sections respectively ([10, 5, 3]), the other has 2 courses, one with 7 sections, the other with 6 sections ([7, 6]), then this function finds we need Course 1 to have 10 section slots, Course 2 to have 6, and Course 3 to have 3.
### process_book
Takes the preset information about a book and checks against all books so far to ensure that it does not already exist, otherwise it adds it to the master list.
### process_courses
Uses the prior get_max_courses function in order to create the headers and add them to the dataframe.
### process_sections
Uses the prior get_max_sections_list function in order to create the individual section headers and adds them to the dataframe.
### process_isbns
This function both finds the max number of ISBN columns required and puts the necessary columns into the dataframe.
### import_data
Imports all the data from the master book object list and imports it into the dataframe once it is ready to go.

## emails.py
Handles compiling and creating Excel sheets for PowerAutomate emails.
### Book (Class)
This class is a very tiny version of the other class that just takes in some basic information for the purposes of emails.
- Constructor
Takes the title, author, edition, year published, and access information.
### Instructor (Class)
- Constructor
Takes in the instructor name, email, as well as course, section, and book information per section.
- add_book
Adds books to a given course section for each professor.
### update_excel
Updates the main sheet with marking off what emails have been successfully created.
### create_email_excel
Processes all the Instructor data to create the table to be used to write it into an Excel sheet.
### write_to_excel
Writes the email data to an Excel sheet to be used with PowerAutomate.

## enrollment.py
Handles pulling the relevant data from the enrollment csv file in order to get the maximum enrollment values.
### get_enrollment_data
Processes the format of the given CORE report enrollment file, returning campus and enrollment information.

## grabber.py
Deals with setting up and handling pulling data from the Outlook browser to get emails for individual professors.
### process_name
### process_suggestion
### get_email
### setup_grabber
### grabber_gui
- set_email_store
- run_process_suggestion
- run_check_ui
- run_check_web
- run_suggestion_ui
- run_get_email
### email_importer
### email_exporter

## gui.py
This hosts all of the primary interactive GUI for the user.
### GUI (Class)
- Constructor
- reset_main
- print_main
- build_main
- build_emails
- build_headers
- build_advanced
- build_sheet_outlook
- build_sheet_alma
- build_sheet_final
- build_import_csv
- start_analytics_csv
- start_bookstore_csv
- start_grabber_csv
- start_mode
- write_cfg
- write_headers
- write_emails
### start_app

## helpergui.py
This is a much slimmer and simpler version of the main GUI class, to be something much more modular and additive.
### AddedGUI (Class)
- Constructor
- reset
- add_label
- add_button
### make_window

## modes.py
Aids in handling the various functions of the script, modularizing individual pieces into useful functions.
### start_mode
### csv_mode
### email_mode
### update_mode
### emails_csv
### analytics_csv
### enrollment_update
### analytics_update
### emails_update
### get_import

## output.py
This script has a single function: outputting an Excel sheet! This is where formatting and such gets handled (i.e. color, column sizing, etc.)
### write_to_sheet

## sheetmaker.py
Performs all of the functions related to creating new sheets from scratch.
### make_excel_sheet

## utilties.py
This script hosts helpful functions that might be purposeful in multiple places around the various helper and main scripts. On top of this, it also helps to host hard coded data that is not necessary to keep in a configuration file (such as header values!). The organization is to help cut down on lines of code in other places, as well as keep information consistency so updating one variable does update it in all relevant places when needed.
### get_int
Takes a value, gets an integer out of it if it can, otherwise returns None.
### get_clean
Removes preset phrases and terms from the names of books and authors to reduce the number of duplicate listings.
### get_state
Takes strings of "True" or "False" and converts them to bool values.
### get_directory
### get_filepath
### get_letter
### get_edition_string
### get_format_headers
### get_replace_header
### get_split_course
### get_input
### get_enabled
### get_sheet_headers
### get_config_headers
### get_string_cleaners
### get_row_info
### get_campus
### set_col_format
A
---
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
---
## Config Files
### config.ini
Primary settings for the script, though some of these are redundant / only used by one half of the script.
### emails.ini
Holds all the template lines for emailing professors.
### headers.ini
Holds all the names of the headers as well as their relation to the internal variable name.