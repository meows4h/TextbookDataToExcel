import unittest
import helpers.analytics as alma
import helpers.bookstore as book
import helpers.classes as classes
import helpers.emails as emails
import helpers.enrollment as enroll
import helpers.grabber as outlook
import helpers.gui as gui
import helpers.helpergui as helpgui
import helpers.modes as modes
import helpers.output as output
import helpers.utilities as util

# skipping selenium oriented functions as they require logging in via the interface
# this could be done in headless mode w/ more looking over the HTML of the log in
# pages, but focusing on the core logic functions for now

# similarly, export and import testing implementations may be done later as they
# likely will not be changing soon and are currently functional

class AnalyticsTest(unittest.TestCase):
    """Testing the analytics.py file."""
    def setUp(self):
        # error message setup
        self.null_msg = "get_columns: Null % SQL Section."
        self.empty_msg = "get_columns: Empty % SQL Section."
        self.missing_msg = "get_columns: Missing Key or Column values in % SQL."
        self.sql_statements = ["SELECT", "FROM", "WHERE", "LIKE"]

    # helper functions

    # checks the SQL columns for proper dictionary setup
    def check_columns(self, columns):
        check = True
        for dict in columns:
            if not dict["Key"] or not dict["Cols"]:
                check = False
                break
        return check
    
    # functionizing the error messages
    def get_sql_msg(self, value):
        new_null = self.null_msg.replace("%", value)
        new_empty = self.empty_msg.replace("%", value)
        new_missing = self.missing_msg.replace("%", value)
        result = {"Null": new_null, "Empty": new_empty, "Miss": new_missing}
        return result

    # testing get_columns
    def test_ebook_sql(self):
        section, columns = alma.get_columns(key="ebook")
        messages = self.get_sql_msg("Ebook")
        
        self.assertIsNotNone(section, messages["Null"])
        self.assertTrue(section, messages["Empty"])

        col_check = self.check_columns(columns)
        self.assertTrue(col_check, messages["Miss"])

    def test_access_sql(self):
        section, columns = alma.get_columns(key="access")
        messages = self.get_sql_msg("Access")
        
        self.assertIsNotNone(section, messages["Null"])
        self.assertTrue(section, messages["Empty"])

        col_check = self.check_columns(columns)
        self.assertTrue(col_check, messages["Miss"])

    def test_physical_sql(self):
        section, columns = alma.get_columns(key="physical")
        messages = self.get_sql_msg("Physical")
        
        self.assertIsNotNone(section, messages["Null"])
        self.assertTrue(section, messages["Empty"])

        col_check = self.check_columns(columns)
        self.assertTrue(col_check, messages["Miss"])
    
    def test_einventory_sql(self):
        section, columns = alma.get_columns(key="e-inventory")
        messages = self.get_sql_msg("E-Inventory")
        
        self.assertIsNotNone(section, messages["Null"])
        self.assertTrue(section, messages["Empty"])

        col_check = self.check_columns(columns)
        self.assertTrue(col_check, messages["Miss"])

    def test_public_sql(self):
        section, columns = alma.get_columns(key="public")
        messages = self.get_sql_msg("Public")
        
        self.assertIsNotNone(section, messages["Null"])
        self.assertTrue(section, messages["Empty"])

        col_check = self.check_columns(columns)
        self.assertTrue(col_check, messages["Miss"])

    # testing get_col_len
    def test_col_len(self):
        # example from real code
        # expects 14 columns
        columns = [
            {
                "Key": "Bibliographic Details",
                "Cols": [
                    "Author",
                    "Title",
                    "ISBN",
                    "Resource Type",
                    "MMS Id",
                    "Earliest Possible Publication Year",
                ],
            },
            {
                "Key": "Physical Item Details",
                "Cols": [
                    "Material Type",
                    "Num of Items (In Repository)",
                    "Temporary Physical Location in Use",
                ],
            },
            {
                "Key": "Holdings Details",
                "Cols": ["Holdings Lifecycle", "Suppressed from Discovery"],
            },
            {"Key": "Edition Simplified", "Cols": ["Edition Simplified (Num)"]},
            {"Key": "Location", "Cols": ["Location Name"]},
            {"Key": "Temporary Location", "Cols": ["Temporary Location Name"]},
        ]
        num = alma.get_col_len(columns)
        expected = 14
        self.assertEqual(num, expected, f"get_col_len: Miscounting column count; expected {expected}, got {num}")

    # selenium functions would go here

    # testing setup_sql
    def test_setup_sql(self):
        col_keys = ["ebook", "access", "physical", "e-inventory", "public"]
        for key_val in col_keys:
            section, columns = alma.get_columns(key=key_val)
            sql = alma.setup_sql(section, columns)
            for command in self.sql_statements:
                self.assertTrue(command in sql, f"setup_sql: {key_val} SQL statement missing {command}")

    # export and import functions would go here


class BookstoreTest(unittest.TestCase):
    """Testing the bookstore.py file."""
    def setUp(self):
        self.clean_msg = "str_clean: Value mismatch from expected; % =/= ^"

    def get_clean_msg(self, res, exp):
        out_msg = self.clean_msg.replace("%", res)
        out_msg = out_msg.replace("^", exp)
        return out_msg

    # testing str_clean
    def test_clean_nl(self):
        new_line = "\nsome text\n\n "
        result = book.str_clean(new_line)
        expected = "some text"
        message = self.get_clean_msg(result, expected)
        self.assertEqual(result, expected, message)

    def test_clean_tab(self):
        tab_char = "\t\thello \t world"
        result = book.str_clean(tab_char)
        expected = "hello world"
        message = self.get_clean_msg(result, expected)
        self.assertEqual(result, expected, message)

    def test_clean_space(self):
        space_text = "   something     a      "
        result = book.str_clean(space_text)
        expected = "something a"
        message = self.get_clean_msg(result, expected)
        self.assertEqual(result, expected, message)

    # get_page_soup selenium function

    # testing get_link

    # get_prices selenium function

    # pull_textbook_data uses selenium

    # pull_data import function


class ClassesTest(unittest.TestCase):
    """Testing the classes.py file."""
    def setUp(self):
        analytics_data = {"Physical MMS Id": {
            "Types": ["Physical"],
            "Copies": [2],
            "Users": [0],
            "CDL": [False],
            "Link": "https://www.example.com",
            "Year": "2024",
            "Location": "Valley Library BIB"
        },
        "Ebook MMS Id": {
            "Types": ["Electronic"],
            "Copies": [0],
            "Users": [4],
            "CDL": [True],
            "Link": "https://www.example2.com",
            "Platform": "",
            "Year": "2020"
        }}
        book_info = {
            "Title": "Book Title",
            "Author": "Book Author",
            "Edition": "Book Edition",
            "Instructor": "Example Name",
            "Email": "Example Email",
            "Course": "Example Course",
            "Section": 1,
            "Enroll": [1, "C"],
            "ISBN": 1,
            "Publisher": "Book Publisher",
            "Req": "Optional",
            "RequiDate": "Requisition Date",
            "Comment": "Example Comment",
            "Analytics": analytics_data,
        }
        self.book = classes.Book(book_info)

    # Book Class testing

    # add_course method
    def test_add_course(self):
        course_name = "Test Course"
        section_num = "999"
        instructor = "Test Name"
        email = "Test Email"
        enroll_data = [99, "D"]

        self.book.add_course(course_name, section_num, instructor, email, enroll_data)
        self.assertEqual(len(self.book.courses), 2, "add_course: Number of courses is incorrect.")
        self.assertEqual(len(self.book.sections), 2, "add_course: Number of sections is incorrect.")
        self.assertEqual(self.book.sec_size[-1], 1, "add_course: Incorrect sec_size array number.")
        self.assertEqual(self.book.total_enroll, 100, "add_course: Total enrollment count is incorrect.")

    # add_section method

    # add_isbn method

    # add_enroll method

    # add_required method

    # End Book Class testing

    # get_max_index testing

    # get_max_courses testing

    # get_max_sections_list testing

    # process_book testing

    # process_sections testing

    # process_isbns testing

    # import_data testing


class EmailsTest(unittest.TestCase):
    """Testing the emails.py file."""

    # Book Class testing

    # Instructor Class testing

    # End Instructor Class testing

    # update_excel testing
    # this needs a setup to run sheetmaker and import other information?

    # create_email_excel testing

    # write_to_excel testing -- this is an export function and should be fine


class EnrollTest(unittest.TestCase):
    """Testing the enrollment.py file."""


class OutlookTest(unittest.TestCase):
    """Testing the grabber.py file."""


class GUITest(unittest.TestCase):
    """Testing the gui.py file."""


class HelperGUITest(unittest.TestCase):
    """Testing the helpergui.py file."""


class ModesTest(unittest.TestCase):
    """Testing the modes.py file."""


class OutputTest(unittest.TestCase):
    """Testing the output.py file."""


class SheetTest(unittest.TestCase):
    """Testing the sheetmaker.py file."""


class UtilTest(unittest.TestCase):
    """Testing the utilities.py file."""
