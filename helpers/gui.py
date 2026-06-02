import tkinter as tk
from tkinter import ttk
import configparser
import threading
from helpers.utilities import get_config_headers, get_directory
from helpers.sheetmaker import make_excel_sheet
from helpers.emails import create_email_excel
from helpers.modes import emails_update, analytics_update, enrollment_update
from helpers.modes import emails_csv, analytics_csv
from helpers.bookstore import pull_textbook_data, pull_info


# the idea here is we compartmentalize the different things into different functions to build screens
# reset screen in each case, store variables on the class scale
class GUI:
    def __init__(self, root):
        self.cfg_path = "config.ini"
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.cfg_path)

        self.root = root
        self.root.title("App Title")
        self.root.minsize(600, 280)
        self.root.maxsize(1680, 540)
        self.tabControl = ttk.Notebook(self.root)

        self.main_tab = ttk.Frame(self.tabControl, padding=(3, 3, 12, 12))
        self.options_tab = ttk.Frame(self.tabControl, padding=(3, 3, 12, 12))
        self.headers_tab = ttk.Frame(self.tabControl, padding=(3, 3, 12, 12))
        self.advanced_tab = ttk.Frame(self.tabControl, padding=(3, 3, 12, 12))

        self.tabControl.add(self.main_tab, text="Main")
        self.tabControl.add(self.options_tab, text="Options")
        self.tabControl.add(self.headers_tab, text="Header Names")
        self.tabControl.add(self.advanced_tab, text="Adv. Options")
        self.tabControl.pack(expand=10, fill="both")

        self.adv_set = {}
        self.opt_set = {}
        self.header_set = {}

        self.build_main()
        self.build_options()
        self.build_advanced()
        self.build_headers()

    # resetting the window
    def reset_main(self):
        for child in self.main_tab.winfo_children():
            child.destroy()

    # used for updating the main screen message
    def print_main(self, message):
        self.reset_main()
        ttk.Label(
            self.main_tab,
            text=message).grid(
            column=0,
            row=0,
            sticky=tk.W)

    # building the main tab
    def build_main(self):
        self.reset_main()
        ttk.Button(
            self.main_tab,
            text="New Sheet",
            command=lambda: self.start_mode(
                flag=1)).grid(
            column=0,
            row=0,
            sticky=tk.E)
        ttk.Button(
            self.main_tab,
            text="CSV",
            command=lambda: self.start_mode(
                flag=2)).grid(
            column=0,
            row=1,
            sticky=tk.E)
        ttk.Button(
            self.main_tab,
            text="Email",
            command=lambda: self.start_mode(
                flag=3)).grid(
            column=0,
            row=2,
            sticky=tk.E)
        ttk.Button(
            self.main_tab,
            text="Update",
            command=lambda: self.start_mode(
                flag=4)).grid(
            column=0,
            row=3,
            sticky=tk.E)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_tab.columnconfigure(2, weight=1)
        for child in self.main_tab.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def build_options(self):
        # probably want to make some tool to make the reading the bookstore numbers and
        # terms easier + easier to modify
        # modifying the output file name
        # otherwise unsure, maybe checkboxes for this?
        ttk.Label(
            self.options_tab,
            text="Putting some easier to modify options here later.").grid(
            column=0,
            row=0,
            sticky=tk.W)

    # building the headers tab
    def build_headers(self):
        header_cfg = get_config_headers()
        max_rows = 8
        col_num = -1
        names = header_cfg["Names"]
        for idx, key in enumerate(names):
            curr_row = idx % max_rows
            if curr_row == 0:
                col_num += 1
                self.headers_tab.columnconfigure(col_num, minsize=240)
            ttk.Label(
                self.headers_tab,
                text=key).grid(
                column=col_num,
                row=curr_row,
                sticky=tk.W)
            self.header_set[key] = tk.StringVar()
            self.header_set[key].set(names[key])
            ttk.Entry(
                self.headers_tab,
                textvariable=self.header_set[key]).grid(
                column=col_num,
                row=curr_row,
                padx=40,
                sticky=tk.E)
        ttk.Button(
            self.headers_tab,
            text="Save to File",
            command=self.write_headers).grid(
            column=0,
            row=max_rows +
            3,
            sticky=tk.W)
        ttk.Label(
            self.headers_tab,
            text="Widen the window to see all the options!").grid(
            column=0,
            row=max_rows + 4,
            sticky=tk.W)

    # building the advanced options tab
    def build_advanced(self):
        max_depth = 0
        for idx, section in enumerate(self.cfg.sections()):
            self.advanced_tab.columnconfigure(idx, minsize=240)
            ttk.Label(self.advanced_tab, text=section).grid(column=idx, row=0)
            for jdx, cfgkey in enumerate(self.cfg[section], 1):
                ttk.Label(
                    self.advanced_tab,
                    text=cfgkey).grid(
                    column=idx,
                    row=jdx,
                    sticky=tk.W)
                key = f"{idx}-{jdx}"
                self.adv_set[key] = tk.StringVar()
                self.adv_set[key].set(
                    self.cfg[section][cfgkey].replace(
                        '%', '%%'))
                ttk.Entry(
                    self.advanced_tab,
                    textvariable=self.adv_set[key]).grid(
                    column=idx,
                    row=jdx,
                    padx=25,
                    sticky=tk.E)
                if jdx + 2 > max_depth:
                    max_depth = jdx + 2
        ttk.Button(
            self.advanced_tab,
            text="Save to File",
            command=self.write_cfg).grid(
            column=0,
            row=max_depth + 1,
            sticky=tk.W,
            columnspan=5)
        ttk.Label(
            self.advanced_tab,
            text="Widen the window to see all the options!").grid(
            column=0,
            row=max_depth + 2,
            sticky=tk.W)

    def build_sheet_outlook(self):
        self.reset_main()
        self.open_outlook = False

        ttk.Label(
            self.main_tab,
            text="Would you like to open Outlook for collecting email addresses?").grid(
            column=0,
            row=0,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="Yes",
            command=lambda: [
                exec("self.open_outlook = True"),
                self.build_sheet_alma()]).grid(
            column=0,
            row=1,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="No",
            command=self.build_sheet_alma).grid(
            column=0,
            row=2,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="Go Back",
            command=self.build_main).grid(
            column=0,
            row=5,
            sticky=tk.W)

    def build_sheet_alma(self):
        self.reset_main()
        self.open_alma = False

        ttk.Label(
            self.main_tab,
            text="Would you like to open Alma for collecting access analytics?").grid(
            column=0,
            row=0,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="Yes",
            command=lambda: [
                exec("self.open_alma = True"),
                self.build_sheet_final()]).grid(
            column=0,
            row=1,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="No",
            command=self.build_sheet_final).grid(
            column=0,
            row=2,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="Go Back",
            command=self.build_sheet_outlook).grid(
            column=0,
            row=5,
            sticky=tk.W)

    def build_sheet_final(self):
        excel_thread = threading.Thread(
            target=lambda: make_excel_sheet(
                self.open_outlook, self.open_alma, self))
        excel_thread.start()
        self.build_main()

    def build_import_csv(self, yes_cmd, no_cmd):
        self.reset_main()
        locals_dict = {"self": self}
        ttk.Label(
            self.main_tab,
            text="Import previous information?").grid(
            column=0,
            row=0,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="Yes",
            command=lambda: exec(yes_cmd, {}, locals_dict)).grid(
            column=0,
            row=1,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="No",
            command=lambda: exec(no_cmd, {}, locals_dict)).grid(
            column=0,
            row=2,
            sticky=tk.W)
        ttk.Button(
            self.main_tab,
            text="Go Back",
            command=lambda: self.start_mode(flag=2)).grid(
            column=0,
            row=5,
            sticky=tk.W)

    def start_analytics_csv(self, import_csv):
        bookstore_cfg = self.cfg["Textbook"]
        textbk_path = get_directory("Save", bookstore_cfg)
        analytics_thread = threading.Thread(target=lambda: analytics_csv(self.cfg, textbk_path, import_csv))
        analytics_thread.start()
        self.build_main()

    def start_bookstore_csv(self):
        bookstore_thread = threading.Thread(target=pull_textbook_data)
        bookstore_thread.start()
        self.build_main()

    def start_grabber_csv(self, import_csv):
        bookstore_cfg = self.cfg["Textbook"]
        textbk_path = get_directory("Save", bookstore_cfg)
        grabber_thread = threading.Thread(target=lambda: emails_csv(self.cfg, textbk_path, import_csv))
        grabber_thread.start()
        self.build_main()

    # function that handles options from the home screen
    def start_mode(self, *args, **kwargs):
        self.reset_main()

        # new sheet
        if kwargs["flag"] == 1:
            self.build_sheet_outlook()

        # csv update
        elif kwargs["flag"] == 2:
            ttk.Label(
                self.main_tab,
                text="What CSV file would you like to update?").grid(
                column=0,
                row=0,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Email Data",
                command=lambda: self.build_import_csv("self.start_grabber_csv(True)", "self.start_grabber_csv(False)")).grid(
                column=0,
                row=1,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Bookstore Data",
                command=self.start_bookstore_csv).grid(
                column=0,
                row=2,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Analytics Data",
                command=lambda: self.build_import_csv("self.start_analytics_csv(True)", "self.start_analytics_csv(False)")).grid(
                column=0,
                row=3,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Go Back",
                command=self.build_main).grid(
                column=0,
                row=5,
                sticky=tk.W)

        # email export
        elif kwargs["flag"] == 3:
            # needs a string var + box
            file_name = tk.StringVar()
            file_name.set("")
            sheet_name = tk.StringVar()
            sheet_name.set("Spring26")
            ttk.Label(
                self.main_tab,
                text="Input which file is being pulled from & updated (i.e. output.xlsx):").grid(
                column=0,
                row=0,
                sticky=tk.W)
            ttk.Entry(
                self.main_tab,
                textvariable=file_name).grid(
                column=0,
                row=1,
                sticky=tk.W)
            ttk.Label(
                self.main_tab,
                text="Input which sheet is being pulled from (i.e. Spring26):").grid(
                column=0,
                row=2,
                sticky=tk.W)
            ttk.Entry(
                self.main_tab,
                textvariable=sheet_name).grid(
                column=0,
                row=3,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Export Sheet",
                command=lambda: create_email_excel(
                    sheet_name.get(),
                    file_name.get())).grid(
                column=0,
                row=4,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Go Back",
                command=self.build_main).grid(
                column=0,
                row=5,
                sticky=tk.W)

        # updating main sheet
        elif kwargs["flag"] == 4:
            # needs a string var + box
            file_name = tk.StringVar()
            file_name.set("")
            sheet_name = tk.StringVar()
            sheet_name.set("Spring26")
            ttk.Label(
                self.main_tab,
                text="Input which file is being updated (i.e. output.xlsx):").grid(
                column=0,
                row=0,
                sticky=tk.W)
            ttk.Entry(
                self.main_tab,
                textvariable=file_name).grid(
                column=0,
                row=1,
                sticky=tk.W)
            ttk.Label(
                self.main_tab,
                text="Input which sheet is being updated (i.e. Spring26):").grid(
                column=0,
                row=2,
                sticky=tk.W)
            ttk.Entry(
                self.main_tab,
                textvariable=sheet_name).grid(
                column=0,
                row=3,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Update Emails",
                command=lambda: emails_update(sheet_name.get())).grid(
                column=0,
                row=5,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Update Analytics",
                command=lambda: analytics_update(sheet_name.get())).grid(
                column=0,
                row=6,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Update Enrollment",
                command=lambda: enrollment_update(sheet_name.get())).grid(
                column=0,
                row=7,
                sticky=tk.W)
            ttk.Button(
                self.main_tab,
                text="Go Back",
                command=self.build_main).grid(
                column=0,
                row=8,
                sticky=tk.W)

    def write_cfg(self):
        for idx, section in enumerate(self.cfg.sections()):
            for jdx, cfgkey in enumerate(self.cfg[section], 1):
                key = f"{idx}-{jdx}"
                self.cfg[section][cfgkey] = self.adv_set[key].get()
        with open(self.cfg_path, 'w') as cfgfile:
            self.cfg.write(cfgfile)

    def write_headers(self):
        cfgdir = "helpers/ini/headers.ini"
        temp_cfg = configparser.ConfigParser()
        temp_cfg.read(cfgdir)
        for key in temp_cfg["Names"]:
            temp_cfg["Names"][key] = self.header_set[key].get()
        with open(cfgdir, 'w') as cfgfile:
            temp_cfg.write(cfgfile)


def start_app():
    root = tk.Tk()
    myapp = GUI(root)
    myapp.root.mainloop()
