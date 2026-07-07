# Documentation File
The goal of this file is to provide a higher level overview of how this script works to help identify issues, improvements, as well as future maintainability.
## At a Glance
There are two primary methods that this script runs through: The CLI version and the GUI version. The CLI version is more or less function complete in how I intend for it to function and operate, though it still has some rough edges, especially in a user interaction factor. The GUI version is what will continue to receive updates and more improvements over time. These two versions can be toggled between in the `config.ini` file.
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
### pull_analytics
### input_sql
### check_element
### click_element
### process_new_isbn
### process_analytics
### setup_analytics
### setup_sql
### export_analytics
### import_analytics

## bookstore.py
Most of this code is pulled from the original bookstore data puller that was made to automate getting bookstore data. It will have the user pass a CAPTCHA and then have them select data to pull from to get the specific term of textbook data they are interested in.
### str_clean
### get_page_soup
### get_link
### get_prices
### pull_textbook_data
### pull_info

## classes.py
Stores the frameworks and methods for interacting with storing and processing book related data.
### Book (Class)
- Contstructor
- add_course
- add_section
- add_isbn
- add_enroll
- add_required
### get_max_index
### get_max_courses
### get_max_sections_list
### process_book
### process_courses
### process_sections
### process_isbns
### import_data

## emails.py
Handles compiling and creating Excel sheets for PowerAutomate emails.
### Book (Class)
- Constructor
### Instructor (Class)
- Constructor
- add_book
### update_excel
### write_to_excel
### create_email_excel

## enrollment.py
Handles pulling the relevant data from the enrollment csv file in order to get the maximum enrollment values.
### get_enrollment_data

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
### get_clean
### get_state
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