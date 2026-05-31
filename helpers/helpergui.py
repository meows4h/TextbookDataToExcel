import tkinter as tk
from tkinter import ttk


# adding an additional gui class to assist with incorporating the other facets of the program more seamlessly
# into the current gui framework without porting everything into seperate
# TKinter scripts
class AddedGUI:
    def __init__(self, title="Context Window"):
        print("Window opened.")
        self.root = tk.Tk()
        self.root.title(title)
        self.root.minsize(400, 100)
        self.root.maxsize(800, 400)
        self.row = 0
        self.column = 0

    def reset(self):
        for child in self.root.winfo_children():
            child.destroy()
        self.row = 0
        self.column = 0

    def add_label(self, message):
        ttk.Label(self.root, text=message).grid(
            column=self.column, row=self.row, sticky=tk.W
        )
        self.row += 1

    def add_button(self, text, cmd):
        ttk.Button(self.root, text=text, command=cmd).grid(
            column=self.column, row=self.row, sticky=tk.W
        )
        self.row += 1


def make_window(title, text):
    gui_window = AddedGUI(title=title)
    gui_window.reset()
    gui_window.add_label(text)
    return gui_window
