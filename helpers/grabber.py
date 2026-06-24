from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
import configparser
import time
import csv
import threading

from helpers.helpergui import AddedGUI
from helpers.utilities import get_directory


def process_name(base, flag):
    """"""
    if flag == 1:
        temp_list = base.split(" ")
        base = ""
        for piece in temp_list:
            if len(piece) > 2:
                base += f"{piece} "

        base = base.strip()
        return base, 2

    # taking first and last listed
    elif flag == 2:
        temp_list = base.split(" ")
        temp_name = f"{temp_list[0]} {temp_list[len(temp_list) - 1]}"
        temp_name = temp_name.strip()
        return temp_name, 3

    # flipping first and last
    elif flag == 3:
        temp_list = base.split(" ")
        temp_name = f"{temp_list[len(temp_list) - 1]} {temp_list[0]}"
        temp_name = temp_name.strip()

        if len(temp_list) > 2:
            return temp_name, 4
        else:
            return temp_name, 10

    # taking first two
    elif flag == 4:
        temp_list = base.split(" ")
        temp_name = f"{temp_list[0]} {temp_list[1]} "
        temp_name = temp_name.strip()
        return temp_name, 10

def process_suggestion(box, len_check=False):
    """Takes the suggestion box element and returns what the top result is."""
    html = box.get_attribute("innerHTML")
    lxml = bs4.BeautifulSoup(html, "lxml")

    li_list = lxml.find_all("li")

    # if the flag is set, if there is more than one result, it will return empty
    # this is to ensure that the correct option is being selected on the first
    # check of the box
    if len(li_list) > 1 and len_check:
        return ""

    for li in li_list:

        # Umn8G is just for the email lines
        list_info = li.find_all("span", class_="MwdHX")
        # could check for name info with list_info[0], some comparison
        if list_info:
            return list_info[1].get_text()
 

def get_email(name, driver):
    """Grabs the first email from the suggestion list
    within the automated browser."""
    break_check = False
    while not break_check:
        try:
            to_box = driver.find_element(By.ID, "0")
            break_check = True
        except BaseException:
            print("Compose box not found.")
            time.sleep(1)

    name = name.replace(",", "")
    name = name.strip()
    base_name = name  # saving name for double checking
    to_box.clear()
    to_box.send_keys(name)

    state = 1
    while True:
        time.sleep(1)
        try:
            suggestion_box = driver.find_element(
                By.CLASS_NAME, "ms-FloatingSuggestionsList-container"
            )
            if state == 1:
                email = process_suggestion(suggestion_box, True)
                if email != "":
                    return email
                else:
                    state = 10
                    raise ValueError("too many / empty box")
            elif state > 10:
                return process_suggestion(suggestion_box)
            else:
                print(base_name)
                checker = input(
                    'Double check the name / email, if incorrect, type "n": '
                )
                # print(checker)
                if checker == "n":
                    # taking it straight to manual if incorrect with listings
                    state = 10
                    raise ValueError("manual error")
                else:
                    return process_suggestion(suggestion_box)

        except (ValueError, NoSuchElementException) as err:
            # this process somewhat works!
            # this needs more refinement / double checking
            # as well as more permutation checking

            # basically if there is only one name in the list on the first case,
            # it will auto take

            # if it goes to any other step, it will require confirmation
            # with changing it requiring the user to be on the manual entry
            # piece

            # if there is no list after manual imput (forcing blank input)
            if state == 11 and isinstance(err, NoSuchElementException):
                return "NO EMAIL"

            if state == 1:
                name, state = process_name(name, state)
                to_box.clear()
                to_box.send_keys(name)

            elif state >= 2 and state <= 4:
                temp_name, state = process_name(name, state)
                to_box.clear()
                to_box.send_keys(temp_name)

            # manual input
            elif state >= 10:
                print(base_name)
                input("Awaiting manual input. (Hit enter when name is ready)")
                state = 11


def setup_grabber():
    """Sets up a selenium browser to pull emails from later."""
    full_config = configparser.ConfigParser()
    full_config.read("config.ini")
    config = full_config["Grabber"]
    link = config["EmailLink"]

    instruction = "Awaiting Outlook Log-in. Open new email compose menu and then leave the window."
    print(instruction)

    driver = webdriver.Chrome()
    driver.get(link)

    break_check = False
    while not break_check:
        time.sleep(5)
        try:
            driver.find_element(By.ID, "0")
            break_check = True
        except BaseException:
            instruction = "Waiting for new email composition window."
            print(instruction)

    return driver


def grabber_gui(textbook_table, email_dict):
    check_state = False
    await_suggest = 0
    email_store = ''
    driver = webdriver.Chrome()

    def set_email_store(value):
        nonlocal email_store
        email_store = value

    def run_process_suggestion(box):
        while True:
            try:
                res_list = []
                html = box.get_attribute("innerHTML")
                lxml = bs4.BeautifulSoup(html, "lxml")

                li_list = lxml.find_all("li")

                for li in li_list:
                    list_info = li.find_all("span", class_="Umn8G")
                    if list_info:
                        res_list.append(list_info[0].get_text())
                
                return res_list
            except:
                # gui_window = AddedGUI(title="Email Grabber Helper")
                # gui_window.add_label(f"No suggestion box. Please search for the email belonging to {name}.")
                # gui_window.add_button("Okay I did that", gui_window.root.destroy)
                # gui_window.root.mainloop()
                print("Error hit in processing suggestion box.")
                time.sleep(1)

    def run_check_ui():
        nonlocal check_state
        gui_window = AddedGUI(title="Email Grabber Helper")
        gui_window.add_label("Waiting for email composition window.")
        gui_window.add_button("Done", gui_window.root.destroy)
        gui_window.root.mainloop()
        check_state = False

    def run_check_web():
        nonlocal check_state
        break_check = False
        while not break_check:
            time.sleep(5)
            try:
                driver.find_element(By.ID, "0")
                break_check = True
            except BaseException:
                if not check_state:
                    check_state = True
                    ui_thread = threading.Thread(target=run_check_ui)
                    ui_thread.start()

    def run_suggestion_ui(name_list, base_name):
        nonlocal await_suggest
        gui_window = AddedGUI(title="Email Grabber Helper")
        gui_window.add_label(f"Which email is correct for {base_name}?")
        for name in name_list:
            gui_window.add_button(f"{name}", lambda n=name: [set_email_store(n), gui_window.root.destroy()])
        gui_window.add_button("No Email", lambda: [set_email_store("NO EMAIL"), gui_window.root.destroy()])
        gui_window.add_button("Refresh Options", lambda: [set_email_store(""), gui_window.root.destroy()])
        gui_window.root.mainloop()
        if await_suggest == 0:
            await_suggest = 1

    def run_get_email(name):
        nonlocal check_state
        nonlocal await_suggest
        break_check = False
        while not break_check:
            time.sleep(5)
            try:
                to_box = driver.find_element(By.ID, "0")
                break_check = True
            except BaseException:
                if not check_state:
                    check_state = True
                    ui_thread = threading.Thread(target=run_check_ui)
                    ui_thread.start()
        
        email_store = ""
        name = name.replace(",", "")
        name = name.strip()
        base_name = name
        to_box.clear()
        to_box.send_keys(name)

        # porting over functions from get_email()
        # can functionize the temp name portions?
        state = 1
        while True:
            time.sleep(0.55)
            try:
                # TODO trying to implement webdriverwait
                # suggestion_box = WebDriverWait(driver, 3).until(
                #     EC.presence_of_element_located((By.CLASS_NAME, "ms-FloatingSuggestionsList-container"))
                # )
                suggestion_box = driver.find_element(
                    By.CLASS_NAME, "ms-FloatingSuggestionsList-container"
                )
                emails = run_process_suggestion(suggestion_box)

                # return email if only one + first
                if len(emails) == 1 and state == 1:
                    return emails[0]
                
                await_suggest = 0
                # i dont think running this as a thread is necessary?
                # to be honest if i reworked this, change these edge case functions that START ui
                # functions to be normal functions, it's just things INSIDE ui need threads
                run_suggestion_ui(emails, base_name)
                if email_store == "":
                    # TODO
                    # if there is a problem with refreshing, double check this
                    state = 10
                    raise ValueError("none of them")
                elif email_store:
                    return email_store
                    
                raise ValueError("shouldn't hit this")
            
            except (ValueError, NoSuchElementException, TimeoutException) as err:
                
                # if state == 11 and (isinstance(err, NoSuchElementException) or isinstance(err, TimeoutException)):
                #     return "NO EMAIL"
                
                if state == 1:
                    name, state = process_name(name, state)
                    to_box.clear()
                    to_box.send_keys(name)

                elif state >= 2 and state <= 4:
                    temp_name, state = process_name(name, state)
                    to_box.clear()
                    to_box.send_keys(temp_name)

                # padding out an extra cycle for more processing time
                elif state == 10:
                    state = 11
                    continue

                elif state >= 11:
                    gui_window = AddedGUI(title="Email Grabber Helper")
                    gui_window.add_label(f"No suggestion box found.")
                    gui_window.add_label(f"Please search for the email belonging to {base_name}.")
                    gui_window.add_label(f"(If there still is one, that's okay! Just press Done)")
                    gui_window.add_button("Done", gui_window.root.destroy)
                    gui_window.root.mainloop()

            except StaleElementReferenceException as err:
                print(err)
  
    full_config = configparser.ConfigParser()
    full_config.read("config.ini")
    config = full_config["Grabber"]
    link = config["EmailLink"]
    emails_path = get_directory("Save", config)

    # start by opening outlook
    driver.get(link)

    # awaiting the time where the user opens the composition window
    check_thread = threading.Thread(target=run_check_web)
    check_thread.start()
    print("Starting check function.")
    check_thread.join()
    print("Check function passed.")

    email_dict["STAFF"] = "NO EMAIL"
    email_dict["STAFF "] = "NO EMAIL"

    for row in textbook_table:
        instructor = row[4]
        if instructor not in email_dict:
            email = run_get_email(instructor)
            email_dict[f"{instructor}"] = email
            email_exporter(emails_path, email_dict)

    email_exporter(emails_path, email_dict)


def email_importer(path):
    """Imports the email csv data given a directory path."""
    email_dict = {}
    with open(path, newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            email_dict[row[0]] = row[1]

    return email_dict


def email_exporter(path, email_dict):
    """Exports to an email csv given the path and data."""
    with open(path, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        for prof in email_dict:
            csvwriter.writerow([f"{prof}"] + [f"{email_dict[prof]}"])
