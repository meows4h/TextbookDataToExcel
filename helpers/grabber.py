from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import bs4
import configparser
import time
import csv
import threading

from helpers.helpergui import AddedGUI


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
                print(checker)
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

            # removing single letter abbreviations + jr, etc
            if state == 1:
                temp_list = name.split(" ")
                name = ""
                for piece in temp_list:
                    if len(piece) > 2:
                        name += f"{piece} "

                name = name.strip()
                to_box.clear()
                to_box.send_keys(name)
                state = 2

            # taking first and last listed
            elif state == 2:
                temp_list = name.split(" ")
                temp_name = f"{temp_list[0]} {temp_list[len(temp_list) - 1]}"
                temp_name = temp_name.strip()
                to_box.clear()
                to_box.send_keys(temp_name)
                state = 3

            # flipping first and last
            elif state == 3:
                temp_list = name.split(" ")
                temp_name = f"{temp_list[len(temp_list) - 1]} {temp_list[0]}"
                temp_name = temp_name.strip()
                to_box.clear()
                to_box.send_keys(temp_name)

                if len(temp_list) > 2:
                    state = 4
                else:
                    state = 10

            # taking first two
            elif state == 4:
                temp_list = name.split(" ")
                temp_name = f"{temp_list[0]} {temp_list[1]} "
                temp_name = temp_name.strip()
                to_box.clear()
                to_box.send_keys(temp_name)
                state = 10

            # manual input
            elif state >= 10:
                print(base_name)
                input("Awaiting manual input. (Hit enter when name is ready)")
                state = 11


# TODO
# finish gui implementation
# temp implementation is an option but need to brainstorm longer about how to fix this
# for now, i say leave it? focus on fixing the analytics implementation?
# or maybe rewrite the whole setup to be in threads instead of blocking
# selenium format. i think that would prove to improve efficiency
def setup_grabber(gui):
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


def grabber_gui(driver_list=[]):
    # global check_state
    # global driver

    # the idea here would be if the driver list is empty
    # we are setting the driver up and using the list to pass it back

    # otherwise we can look at the information we are wanting to 
    # get the email from / with ?

    # alternatively, we can pass in the entire section of data that
    # we are needing to manage and let it run from start to finish
    # in a thread all by itself instead of going back and forth
    
    # latter option probably better
    if driver_list == []:
        check_state = False
        driver = webdriver.Chrome()
        driver_list.append(driver)

    # def run_get_email():

    def run_check_web(driver):
        # global check_state
        break_check = False
        while not break_check:
            time.sleep(5)
            try:
                driver.find_element(By.ID, "0")
                break_check = True
            except BaseException:
                instruction = "Waiting for new email composition window."
                if not check_state:
                    check_state = True
                    ui_thread = threading.Thread(target=run_ui)
                    ui_thread.start()
    
    def run_ui():
        # global check_state
        gui_window = AddedGUI(title="Email Grabber Helper")
        gui_window.add_label("Some text")
        gui_window.add_button("Okay im done", gui_window.root.destroy)
        gui_window.root.mainloop()
        check_state = False

    full_config = configparser.ConfigParser()
    full_config.read("config.ini")
    config = full_config["Grabber"]
    link = config["EmailLink"]
    driver.get(link)
    check_thread = threading.Thread(target=lambda: run_check_web(driver))
    check_thread.start()
    print("Waiting 1")
    check_thread.join()
    print("Waiting 2")


def start_browser():
    print("test")
    # maybe port some of the selenium setup code into this code
    # block, then run it out of the threads?
    # if the threads are able to report back values, it can send
    # values into the other GUI thread block which will help with
    # the start stopping of everything?
    # examples:

    def task(name):
        print(f"Task {name} starting...")
        time.sleep(2)  # Simulates an I/O wait
        print(f"Task {name} finished!")

    # 1. Create threads
    t1 = threading.Thread(target=task, args=("A",))
    t2 = threading.Thread(target=task, args=("B",))

    # 2. Start execution
    t1.start()
    t2.start()

    # 3. Wait for threads to finish before continuing the main program
    t1.join()
    t2.join()

    print("All tasks done.")

    def run_selenium():
        # This function runs in a separate thread to keep the GUI responsive
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        # Add your automation steps here
        print("Page Title:", driver.title)
        # driver.quit()

    def start_thread():
        # Start Selenium in a new thread
        thread = threading.Thread(target=run_selenium)
        thread.start()

    root = tk.Tk()
    root.title("Automation Tool")
    root.geometry("300x150")

    btn = tk.Button(root, text="Start Browser", command=start_thread)
    btn.pack(pady=20)

    root.mainloop()


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
