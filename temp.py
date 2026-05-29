import tkinter as tk
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import bs4
import configparser
import time
import csv
import threading

from helpers.helpergui import AddedGUI


def run_selenium():
    # This function runs in a separate thread to keep the GUI responsive
    global check_state
    global driver
    check_state = False
    driver = webdriver.Chrome()

    # Add your automation steps here
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

    # driver.quit()


def run_get_email():
    global driver


def run_check_web(driver):
    global check_state
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
    global check_state
    gui_window = AddedGUI(title="Email Grabber Helper")
    gui_window.add_label("Some text")
    gui_window.add_button("Okay im done", gui_window.root.destroy)
    gui_window.root.mainloop()
    check_state = False


def start_thread():
    thread = threading.Thread(target=run_selenium)
    thread.start()
    return thread


# root = AddedGUI("New Window")
# root.add_button("Do the thing", start_thread)
# root.root.mainloop()
