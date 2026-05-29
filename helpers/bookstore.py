from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.window import WindowTypes
import time
import bs4
import configparser
import csv
from helpers.utilities import get_state, get_directory


def str_clean(str):
    """"""
    new_str = str.replace("&nbsp;", "")
    new_str = new_str.replace("  ", "")
    new_str = new_str.replace("\t", "")
    new_str = new_str.replace("\n", "")
    return new_str


def get_page_soup(driver, url):
    """"""
    driver.get(url)
    html_content = driver.page_source
    page = bs4.BeautifulSoup(html_content, "lxml")
    return page


def get_link(link, term, subject, code, section):
    """"""
    link = link.replace("TERM", f"{term}")
    link = link.replace("SUBJECT", f"{subject}")
    link = link.replace("CODE", f"{code}")
    link = link.replace("SECTION", f"{section}")
    return link


def get_row_price(driver, row, link):
    """"""
    term = row[0]
    department = row[1]
    dep_arr = department.split(":")
    subj_code = dep_arr[0].strip()
    subj_num = row[2]
    section = row[3]
    isbn = row[8].replace("-", "").strip()
    link = get_link(link, term, subj_code, subj_num, section)

    price = ""

    base_window = driver.current_window_handle
    driver.switch_to.new_window(WindowTypes.TAB)
    driver.get(link)

    try:
        WebDriverWait(
            driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "item")))
        materials = driver.find_elements(By.CLASS_NAME, "item")
        book_found = False
        main_div = None
        for material in materials:
            html = material.get_attribute("innerHTML")
            lxml = bs4.BeautifulSoup(html, "lxml")
            td_list = lxml.find_all("td")
            for td in td_list:
                if td.get_text() == isbn:
                    book_found = True
                    main_div = material
                    break
            if book_found:
                break

        if book_found:
            main_div.click()
            # TODO left off here!
            # this needs to pull the used and new price points from the beaverstore page
            # https://osubeaverstore.verbacompare.com/comparison?id=2026-Summer__AEC__411__400
    except Exception as err:
        print(err)

    driver.close()
    driver.switch_to.window(base_window)
    return price


def pull_textbook_data():
    """Pulls textbook data from the given webpage and returns
    the output table."""

    # configure this script using the .ini file
    full_config = configparser.ConfigParser()
    full_config.read("config.ini")
    config = full_config["Textbook"]
    output = get_state(config["Output"])
    # whether or not to skip lines with 'SEE CANVAS AND/OR INSTRUCTOR FOR
    # COURSE MATERIALS - NO COST' in them
    nocost_skip = get_state(config["NoCostSkip"])
    save_file = get_state(config["Save"])
    textbk_path = get_directory("Save", config)
    custom_term = [config["CustomNum"], config["CustomName"]]

    # gets chrome tab
    driver = webdriver.Chrome()

    # the following bit automatically checks for the captcha completion by
    # determining whether or not there is a readable table in the html, in
    # which the captcha page does not
    print("Awaiting CAPTCHA completion.")

    list_link = "https://beavs.osubeaverstore.com/Textbooks.asp"
    store_link = "https://osubeaverstore.verbacompare.com/comparison?id=TERM__SUBJECT__CODE__SECTION"

    driver.get(list_link)
    exit_check = False
    term_int = 0

    while not exit_check:
        captcha_html = driver.page_source
        captcha_page = bs4.BeautifulSoup(captcha_html, "lxml")
        if captcha_page.find_all("td"):
            exit_check = True
            print("CAPTCHA passed!")
        time.sleep(2)

    # grabs html content and gets csv fields ready
    html_content = driver.page_source
    table_export = []
    curr_page = bs4.BeautifulSoup(html_content, "lxml")
    terms = [custom_term]

    # asking the user which terms they would wish to pull
    # while True:
    #     try:
    #         term_int = int(
    #             input(
    #                 "Which terms would you like to pull?\n 1 - All\n 2 - Most Recent\n 3 - Custom (Defined in Code)\n Select one: "
    #             )
    #         )
    #         if 0 < term_int < 4:
    #             break
    #         else:
    #             raise TypeError
    #     except TypeError:
    #         print("Please select one of the correct options.\n")
    #         continue
    #     except ValueError:
    #         print("Please select one of the correct options.\n")
    #         continue

    # gets all the term values and their names
    # if term_int == 1:
    #     for td in curr_page.find_all("td"):

    #         if skip_check == 0:
    #             skip_check = 1
    #             continue

    #         skip_check = 0

    #         for option in td.find_all("option"):

    #             if skip_check == 0:
    #                 skip_check = 1
    #                 continue

    #             terms.append([option["value"], option.text])

    # if term_int == 2:

    #     for td in curr_page.find_all("td"):

    #         if skip_check == 0:
    #             skip_check = 1
    #             continue

    #         skip_check = 0

    #         for option in td.find_all("option"):

    #             if skip_check == 0:
    #                 skip_check = 1
    #                 continue

    #             terms.append([option["value"], option.text])
    #             break

    #         break

    # if term_int == 3:

    #     # to add a custom term, please insert a 'terms.append()' function here
    #     # the list to append takes the format of [value, "name"]
    #     # the value can be found within the HTML of the page, in the option
    #     # element of the term you wish to extract

    #     terms.append(custom_term)

    print(f"Searching through set terms: {terms}")

    # iterates through every term
    for term in terms:

        curr_page = get_page_soup(
            driver,
            f"https://beavs.osubeaverstore.com/Textbooks.asp?TermID={term[0]}"
        )

        departments = []

        for num, tr in enumerate(curr_page.find_all("tr")):
            if num == 0:
                continue

            for num2, option in enumerate(tr.find_all("option")):
                if num2 == 0:
                    continue

                # appends the department information for each term in case it
                # changes over time
                departments.append([option["value"], option.text])

        if output:
            print(f"Departments found for {term[1]}.")

        # goes through each department
        for department in departments:
            curr_page = get_page_soup(
                driver,
                f"https://beavs.osubeaverstore.com/Textbooks.asp?TermID={
                    term[0]}&DeptID={
                    department[0]}")

            # for all the tables
            for num, table in enumerate(curr_page.find_all("table")):

                # if it is the first one, go to the next table (bypassing the
                # header)
                if num == 0:
                    continue

                # in the body of all of these tables
                for tbody in table.find_all("tbody"):

                    # in each row
                    for row in tbody.find_all("tr"):

                        row_skip = 0
                        # holds text for the row itself
                        row_text = []

                        term_app = str_clean(term[1])
                        dep_app = str_clean(department[1])
                        row_text.append(f"{term_app}")
                        row_text.append(f"{dep_app}")

                        # for each cell in the row
                        for cell in row.find_all("td"):

                            text = str_clean(cell.text)
                            if (
                                text
                                == "SEE CANVAS AND/OR INSTRUCTOR FOR COURSE MATERIALS - NO COST "
                                and nocost_skip
                            ):
                                row_skip = 1
                                break
                            row_text.append(text)

                        # append the row to the master matrix
                        if row_skip == 0:
                            # commenting out for now to run new data pulling
                            # row_text.append(
                            #     get_row_price(
                            #         driver, row_text, store_link))
                            table_export.append(row_text)

            # logging text
            dpt_txt = str_clean(f"{department[1]}")
            if output:
                print(f"{dpt_txt} complete.")

        # formatting output
        if output:
            print("\n")

    # open an output csv file and then write the header into it before writing
    # every list element (row data) as a row in the csv file
    if save_file:
        with open(textbk_path, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            # csvwriter.writerow(fields)
            csvwriter.writerows(table_export)

    return table_export


def pull_info(path):
    """Pulls info from the given path to import as the bookstore data."""
    table_export = []
    with open(path, newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            table_export.append(row)

    return table_export
