# A Metadata Editor for Steam Applications
# Copyright (C) 2023  Tomás Ralph
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
from copy import deepcopy
from datetime import datetime
from json import JSONDecodeError

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Treeview, Style

from config import config
from appinfo import Appinfo

from gui.widgets import (
    Frame,
    Button,
    DeleteButton,
    LabelFrame,
    Label,
    Entry,
    Checkbutton,
    Scrollbar,
    ScrollableFrame,
)


class MainWindow:
    def __init__(self):
        self.modifiedApps = []
        silent = config.silent
        export = config.export
        self.vdf_path = os.path.join(
            config.STEAM_PATH, "appcache", "appinfo.vdf"
        )

        if export is not None:
            self.modifiedApps.extend(export)
            self.load_modifications()
            self.appinfo = Appinfo(
                self.vdf_path, True, apps=self.modifiedApps
            )

            for app in self.modifiedApps:
                self.save_original_data(app)

            self.write_modifications()

        if silent:
            self.load_modifications()
            self.appinfo = Appinfo(
                self.vdf_path, True, apps=self.modifiedApps
            )

            for app in self.modifiedApps:
                self.appinfo.parsedAppInfo[app]["sections"] = self.jsonData[
                    str(app)
                ]["modified"]

            self.write_data_to_appinfo(notice=False)

        if not silent and export is None:
            self.create_main_window()

            for app in self.modifiedApps:
                self.appinfo.parsedAppInfo[app]["sections"] = self.jsonData[
                    str(app)
                ]["modified"]

    def create_main_window(self):
        # Define main window
        self.window = tk.Tk()
        self.window.title("Steam Metadata Editor")
        self.window.resizable(width=False, height=False)
        self.window.config(padx=10, pady=10, bg=config.BG)

        # Hide to show loading window
        self.window.withdraw()
        loadingWindow = LoadingWindow(self.window)

        # Load appinfo
        self.appinfo = Appinfo(self.vdf_path)

        # Button images
        self.upArrowImage = tk.PhotoImage(file=f"{config.IMG_PATH}/UpArrow.png")
        self.downArrowImage = tk.PhotoImage(file=f"{config.IMG_PATH}/DownArrow.png")
        self.deleteImage = tk.PhotoImage(file=f"{config.IMG_PATH}/Delete.png")

        # Treeview style
        self.treeviewStyle = Style()
        self.treeviewStyle.configure(
            "Treeview",
            font=(config.FONT, 9),
            background=config.ENTRY_BG,
            foreground=config.ENTRY_FG,
            fieldbackground=config.ENTRY_BG,
            rowheight=20,
            relief=config.ENTRY_RELIEF,
        )
        self.treeviewStyle.configure(
            "Treeview.Heading",
            font=(config.FONT, 10),
            background=config.BG,
            foreground=config.FG,
            relief=config.ENTRY_RELIEF,
        )

        # String vars
        self.idVar = tk.StringVar()
        self.nameVar = tk.StringVar()
        self.sortAsVar = tk.StringVar()
        self.developerVar = tk.StringVar()
        self.publisherVar = tk.StringVar()
        self.ogRelease1Var = tk.StringVar()
        self.ogRelease2Var = tk.StringVar()
        self.ogRelease3Var = tk.StringVar()
        self.steamRelease1Var = tk.StringVar()
        self.steamRelease2Var = tk.StringVar()
        self.steamRelease3Var = tk.StringVar()
        self.searchBarVar = tk.StringVar()

        # Layout setup
        self.leftFrame = LabelFrame(
            self.window, padx=10, pady=10, text="Search:"
        )
        self.rightContainerFrame = Frame(self.window, padx=10, pady=10)
        # Label specific
        self.rightIdFrame = Frame(self.rightContainerFrame)
        self.rightNameFrame = Frame(self.rightContainerFrame)
        self.rightSortAsFrame = Frame(self.rightContainerFrame)
        self.rightDeveloperFrame = Frame(self.rightContainerFrame)
        self.rightPublisherFrame = Frame(self.rightContainerFrame)
        self.rightOgReleaseFrame = Frame(self.rightContainerFrame)
        self.rightSteamReleaseFrame = Frame(self.rightContainerFrame)
        self.buttonsFrame = Frame(self.rightContainerFrame)

        # Widgets (left side)
        self.searchBar = Entry(
            self.leftFrame,
            textvariable=self.searchBarVar,
        )
        self.searchBarVar.trace_add(
            "write", lambda _a, _b, _c: self.locate_app_in_list()
        )
        self.searchBar.focus()

        self.appListScrollbar = Scrollbar(self.leftFrame)

        self.appList = Treeview(self.leftFrame, columns=("Type", "Mod", "ID"))
        self.appList.heading("#0", text="App Name")
        self.appList.heading("Type", text="Type")
        self.appList.heading("Mod", text="Modified")
        self.appList.heading("ID", text="ID")
        self.appList.column("#0", width=300, stretch=False)
        self.appList.column("Type", width=50, minwidth=20)
        self.appList.column("Mod", width=55, minwidth=20)
        self.appList.column("ID", width=80, minwidth=80)
        self.appList.bind("<<TreeviewSelect>>", self.fetch_app_data)

        # Widgets (right side)
        self.idLabel = Label(self.rightIdFrame, text="ID:")
        self.idEntry = Entry(
            self.rightIdFrame,
            width=40,
            textvariable=self.idVar,
            state="readonly",
        )

        self.nameLabel = Label(self.rightNameFrame, text="Name:")
        self.nameEntry = Entry(
            self.rightNameFrame,
            width=40,
            textvariable=self.nameVar,
        )

        self.sortAsLabel = Label(self.rightSortAsFrame, text="Sort As:")
        self.sortAsEntry = Entry(
            self.rightSortAsFrame,
            width=40,
            textvariable=self.sortAsVar,
        )

        self.developerLabel = Label(
            self.rightDeveloperFrame,
            text="Developer:",
        )
        self.developerEntry = Entry(
            self.rightDeveloperFrame,
            width=40,
            textvariable=self.developerVar,
        )

        self.publisherLabel = Label(
            self.rightPublisherFrame,
            text="Publisher:",
        )
        self.publisherEntry = Entry(
            self.rightPublisherFrame,
            width=40,
            textvariable=self.publisherVar,
        )

        self.ogReleaseLabel = Label(
            self.rightOgReleaseFrame,
            text="Original Release Date:",
        )
        self.ogReleaseEntry1 = Entry(
            self.rightOgReleaseFrame,
            width=4,
            textvariable=self.ogRelease1Var,
        )
        self.ogReleaseEntry2 = Entry(
            self.rightOgReleaseFrame,
            width=2,
            textvariable=self.ogRelease2Var,
        )
        self.ogReleaseEntry3 = Entry(
            self.rightOgReleaseFrame,
            width=2,
            textvariable=self.ogRelease3Var,
        )

        self.steamReleaseLabel = Label(
            self.rightSteamReleaseFrame,
            text="Steam Release Date:",
        )
        self.steamReleaseEntry1 = Entry(
            self.rightSteamReleaseFrame,
            width=4,
            textvariable=self.steamRelease1Var,
        )
        self.steamReleaseEntry2 = Entry(
            self.rightSteamReleaseFrame,
            width=2,
            textvariable=self.steamRelease2Var,
        )
        self.steamReleaseEntry3 = Entry(
            self.rightSteamReleaseFrame,
            width=2,
            textvariable=self.steamRelease3Var,
        )

        self.launchMenuButton = Button(
            self.buttonsFrame,
            text="Edit launch menu",
            command=self.create_launch_menu_window,
        )
        self.revertAppButton = Button(
            self.buttonsFrame,
            text="Revert App",
            command=lambda: self.revert_app(self.idVar.get()),
        )
        self.saveButton = Button(
            self.buttonsFrame,
            text="Save",
            command=self.write_data_to_appinfo,
        )

        # Pack widgets (left side)
        self.searchBar.pack(side="top", fill="both", pady=(0, 10))
        self.appListScrollbar.pack(side="right", fill="both")
        self.appList.pack(side="top", fill="both")

        # Pack widgets (right side)
        self.idLabel.pack(side="left")
        self.idEntry.pack(side="right")
        self.nameLabel.pack(side="left")
        self.nameEntry.pack(side="right")
        self.sortAsLabel.pack(side="left")
        self.sortAsEntry.pack(side="right")
        self.developerLabel.pack(side="left")
        self.developerEntry.pack(side="right")
        self.publisherLabel.pack(side="left")
        self.publisherEntry.pack(side="right")

        self.ogReleaseLabel.pack(side="left")
        self.ogReleaseEntry3.pack(side="right", padx=(10, 0))
        self.ogReleaseEntry2.pack(side="right", padx=10)
        self.ogReleaseEntry1.pack(side="right", padx=(0, 10))

        self.steamReleaseLabel.pack(side="left")
        self.steamReleaseEntry3.pack(side="right", padx=(10, 0))
        self.steamReleaseEntry2.pack(side="right", padx=10)
        self.steamReleaseEntry1.pack(side="right", padx=(0, 10))

        self.launchMenuButton.pack(side="left")
        self.revertAppButton.pack(side="left")
        self.saveButton.pack(side="right")

        # Frames
        self.leftFrame.pack(side="left", fill="both")
        self.rightContainerFrame.pack(side="right", fill="both")

        self.rightIdFrame.pack(
            side="top", fill="both", pady=(0, config.ENTRY_PADDING)
        )
        self.rightNameFrame.pack(side="top", fill="both", pady=config.ENTRY_PADDING)
        self.rightSortAsFrame.pack(side="top", fill="both", pady=config.ENTRY_PADDING)
        self.rightDeveloperFrame.pack(
            side="top", fill="both", pady=config.ENTRY_PADDING
        )
        self.rightPublisherFrame.pack(
            side="top", fill="both", pady=config.ENTRY_PADDING
        )
        self.rightOgReleaseFrame.pack(
            side="top", fill="both", pady=config.ENTRY_PADDING
        )
        self.rightSteamReleaseFrame.pack(
            side="top", fill="both", pady=(config.ENTRY_PADDING, 0)
        )
        self.buttonsFrame.pack(side="bottom", fill="both")

        # Extra config
        self.appList.config(yscrollcommand=self.appListScrollbar.set)
        self.appListScrollbar.config(command=self.appList.yview)

        self.load_modifications()
        self.mark_installed_games()
        self.populate_app_list()

        # Destroy loading window and show main one
        # after appinfo finishes loading
        loadingWindow.destroy()
        self.window.deiconify()

        # Center window
        self.window.update()
        self.window.update_idletasks()
        self.center_window(self.window)

    def mark_installed_games(self):
        lbryPath = os.path.join(config.STEAM_PATH, "steamapps", "libraryfolders.vdf")
        with open(lbryPath, "r") as libraries:
            contents = libraries.read()
            libraries = config.PATH_REGEX.findall(contents)
            apps = [int(x) for x in config.APP_REGEX.findall(contents)]

        for library in libraries:
            for app in apps:
                install_dir = self.get_data_from_section(
                    app, "config", "installdir"
                )
                install_path = os.path.join(
                    library, "steamapps", "common", install_dir
                )
                if not os.path.exists(install_path):
                    continue
                self.appinfo.parsedAppInfo[app]["installed"] = True
                self.appinfo.parsedAppInfo[app][
                    "install_path"
                ] = install_path

    def write_modifications(self):
        with open(f"{config.CONFIG_PATH}/modifications.json", "w") as mod:
            for app in self.modifiedApps:
                self.jsonData[str(app)][
                    "modified"
                ] = self.appinfo.parsedAppInfo[app]["sections"]
            json.dump(self.jsonData, mod, indent=2)

    def save_original_data(self, appID):
        appData = deepcopy(self.appinfo.parsedAppInfo[appID]["sections"])
        self.jsonData[str(appID)] = {}
        self.jsonData[str(appID)]["original"] = appData

    def load_modifications(self):
        try:
            with open(f"{config.CONFIG_PATH}/modifications.json", "r") as mod:
                self.jsonData = json.load(mod)
                for app in self.jsonData:
                    app = int(app)
                    if app not in self.modifiedApps:
                        self.modifiedApps.append(app)
        except (FileNotFoundError, JSONDecodeError):
            self.jsonData = {}

    def get_data_from_section(self, appID, *sections, error=""):
        data = self.appinfo.parsedAppInfo[appID]["sections"]["appinfo"]
        for section in sections:
            try:
                data = data[section]
            except KeyError:
                return error

        return data

    # Given a var, it removes the callback, sets the value
    # and reassigns the callback
    def set_var_no_callback(self, var, value, callback):
        try:
            callbackId = var.trace_vinfo()[0][1]
            var.trace_remove("write", callbackId)
        except IndexError:
            pass

        var.set(value)
        var.trace_add("write", callback)

    def set_data_from_section(self, appID, value, *sections):
        appID = int(appID)

        if appID not in self.modifiedApps:
            self.save_original_data(appID)
            self.modifiedApps.append(appID)

        data = self.appinfo.parsedAppInfo[appID]["sections"]["appinfo"]
        # Access all but the last element
        for section in sections[0:len(sections) - 1]:
            try:
                data = data[section]
            except KeyError:
                data[section] = {}
                data = data[section]

        data[sections[-1]] = value

    def get_unix_time(self, year, month, day):
        return int(datetime(year, month, day).timestamp())

    def set_timestamps(self, stampId):
        appID = int(self.idVar.get())

        def validate_date_format(year, month, day):
            if len(str(year)) > 4 or year < 1970:
                return False
            try:
                if datetime(year, month, day) > datetime.today():
                    return False
            except ValueError:
                return False

            return True

        if stampId == "original":

            try:
                year = int(self.ogRelease1Var.get())
                month = int(self.ogRelease2Var.get())
                day = int(self.ogRelease3Var.get())
            # This happens when the field is empty
            except ValueError:
                return

            if validate_date_format(year, month, day):

                appOgReleaseDate = self.get_unix_time(year, month, day)
                self.set_data_from_section(
                    appID, appOgReleaseDate, "common", "original_release_date"
                )
        elif stampId == "steam":

            try:
                year = int(self.steamRelease1Var.get())
                month = int(self.steamRelease2Var.get())
                day = int(self.steamRelease3Var.get())
            # This happens when the field is empty
            except ValueError:
                return

            if validate_date_format(year, month, day):

                appSteamReleaseDate = self.get_unix_time(year, month, day)
                self.set_data_from_section(
                    appID, appSteamReleaseDate, "common", "steam_release_date"
                )

    def write_data_to_appinfo(self, notice=True):
        self.write_modifications()

        for appId in self.modifiedApps:
            self.appinfo.update_app(appId)

        self.appinfo.write_data()

        if notice:
            messagebox.showinfo(
                title="Success!",
                message="Your changes " + "have been successfully applied!",
            )

    def revert_app(self, appId):
        appId = int(appId)

        if appId in self.modifiedApps:
            if messagebox.askyesno(
                title="Revert Game",
                message="Are you "
                + "sure you want to revert this game? All your "
                + "modifications will be erased, this cannot be undone.",
            ):

                # Fetch original data and replace it
                originalData = deepcopy(self.jsonData[str(appId)]["original"])
                self.appinfo.parsedAppInfo[appId]["sections"] = originalData

                # Delete app from modified apps
                # to not save it in the json again
                if appId in self.modifiedApps:
                    self.modifiedApps.remove(appId)

                # Delete data from json
                del self.jsonData[str(appId)]
                self.write_modifications()

                self.appinfo.update_app(appId)
                self.appinfo.write_data()

                # Update app list
                self.appList.delete(*self.appList.get_children())
                self.populate_app_list()

    def fetch_app_data(self, _event):
        # Data from list
        currentItem = self.appList.focus()
        currentItemData = self.appList.item(currentItem)
        appID = currentItemData["values"][-1]
        # Fetched data
        appName = self.get_data_from_section(appID, "common", "name")
        appSortAs = self.get_data_from_section(appID, "common", "sortas")
        appDeveloper = self.get_data_from_section(
            appID, "extended", "developer"
        )
        appPublisher = self.get_data_from_section(
            appID, "extended", "publisher"
        )
        appSteamReleaseDate = self.get_data_from_section(
            appID, "common", "steam_release_date"
        )
        appOgReleaseDate = self.get_data_from_section(
            appID, "common", "original_release_date"
        )

        if not appSteamReleaseDate:
            appSteamReleaseDate = 0
        if not appOgReleaseDate:
            appOgReleaseDate = appSteamReleaseDate
        if not appSortAs:
            appSortAs = appName

        appSteamReleaseDate = datetime.fromtimestamp(appSteamReleaseDate)
        appOgReleaseDate = datetime.fromtimestamp(appOgReleaseDate)

        self.idVar.set(appID)

        self.set_var_no_callback(
            self.nameVar,
            appName,
            lambda _a, _b, _c: (
                self.set_data_from_section(
                    int(self.idVar.get()), self.nameVar.get(), "common", "name"
                ),
                self.sortAsVar.set(self.nameVar.get()),
            ),
        )

        self.set_var_no_callback(
            self.sortAsVar,
            appSortAs,
            lambda _a, _b, _c: self.set_data_from_section(
                int(self.idVar.get()), self.sortAsVar.get(), "common", "sortas"
            ),
        )

        self.set_var_no_callback(
            self.developerVar,
            appDeveloper,
            lambda _a, _b, _c: (
                self.set_data_from_section(
                    int(self.idVar.get()),
                    self.developerVar.get(),
                    "extended",
                    "developer",
                ),
                self.set_data_from_section(
                    int(self.idVar.get()),
                    self.developerVar.get(),
                    "common",
                    "associations",
                    "0",
                    "name",
                ),
            ),
        )

        self.set_var_no_callback(
            self.publisherVar,
            appPublisher,
            lambda _a, _b, _c: (
                self.set_data_from_section(
                    int(self.idVar.get()),
                    self.publisherVar.get(),
                    "extended",
                    "publisher",
                ),
                self.set_data_from_section(
                    int(self.idVar.get()),
                    self.publisherVar.get(),
                    "common",
                    "associations",
                    "1",
                    "name",
                ),
            ),
        )

        self.set_var_no_callback(
            self.ogRelease1Var,
            f"{appOgReleaseDate:%Y}",
            lambda _a, _b, _c: self.set_timestamps("original"),
        )
        self.set_var_no_callback(
            self.ogRelease2Var,
            f"{appOgReleaseDate:%m}",
            lambda _a, _b, _c: self.set_timestamps("original"),
        )
        self.set_var_no_callback(
            self.ogRelease3Var,
            f"{appOgReleaseDate:%d}",
            lambda _a, _b, _c: self.set_timestamps("original"),
        )

        self.set_var_no_callback(
            self.steamRelease1Var,
            f"{appSteamReleaseDate:%Y}",
            lambda _a, _b, _c: self.set_timestamps("steam"),
        )
        self.set_var_no_callback(
            self.steamRelease2Var,
            f"{appSteamReleaseDate:%m}",
            lambda _a, _b, _c: self.set_timestamps("steam"),
        )
        self.set_var_no_callback(
            self.steamRelease3Var,
            f"{appSteamReleaseDate:%d}",
            lambda _a, _b, _c: self.set_timestamps("steam"),
        )

    def insert_app_in_list(self, app):
        self.appList.insert(
            parent="",
            index="end",
            text=app[0],
            values=(app[1], app[2], app[3]),
        )

    def locate_app_in_list(self):
        query = self.searchBar.get().lower()

        # Clear list to fill it with results
        self.appList.delete(*self.appList.get_children())

        if query:
            for app in self.appData:
                if query in app[0].lower():
                    self.insert_app_in_list(app)
        else:
            # Update app list
            self.populate_app_list()

    def center_window(self, window):
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()
        windowWidth = window.winfo_reqwidth()
        windowHeight = window.winfo_reqheight()

        windowX = (screenWidth / 2) - (windowWidth / 2)
        windowY = (screenHeight / 2) - (windowHeight / 2)

        window.geometry(
            f"{windowWidth}x{windowHeight}+" + f"{int(windowX)}+{int(windowY)}"
        )

    def ask_to_create_launch_option(self, appID):
        self.launchMenuWindow.withdraw()
        answer = messagebox.askyesno(
            "No Launch Options",
            "This app has no launch options. Do you wish to create one?",
        )
        if answer:
            self.add_launch_option(appID)
            self.launchMenuWindow.deiconify()
        else:
            self.launchMenuWindow.destroy()

    def move_launch_option(self, appID, optionNumber, direction):
        launchOption = self.get_data_from_section(
            appID, "config", "launch", optionNumber
        )

        if direction == "up":
            newOptionNumber = str(int(optionNumber) - 1)
            # Check if the location exists
            nextLaunchOption = self.get_data_from_section(
                appID, "config", "launch", newOptionNumber
            )

            if nextLaunchOption is not False:
                self.set_data_from_section(
                    appID, nextLaunchOption, "config", "launch", optionNumber
                )
                self.set_data_from_section(
                    appID, launchOption, "config", "launch", newOptionNumber
                )
            else:
                return
            self.update_launch_menu_window(appID)
        elif direction == "down":
            newOptionNumber = str(int(optionNumber) + 1)
            # Check if the location exists
            prevLaunchOption = self.get_data_from_section(
                appID, "config", "launch", newOptionNumber
            )

            if prevLaunchOption is not False:
                self.set_data_from_section(
                    appID, prevLaunchOption, "config", "launch", optionNumber
                )
                self.set_data_from_section(
                    appID, launchOption, "config", "launch", newOptionNumber
                )
            else:
                return
            self.update_launch_menu_window(appID)
        else:
            return

    def delete_launch_option(self, appID, optionNumber):
        launchOptions = self.get_data_from_section(appID, "config", "launch")

        found = False
        keys = list(launchOptions.keys())
        for launchOption in keys:
            if not found:
                if launchOption == optionNumber:
                    found = True
            else:
                newOptionNumber = str(int(launchOption) - 1)
                self.set_data_from_section(
                    appID,
                    launchOptions[launchOption],
                    "config",
                    "launch",
                    newOptionNumber,
                )
        del launchOptions[keys[-1]]
        self.update_launch_menu_window(appID)

    def add_launch_option(self, appID):
        launchOptions = self.get_data_from_section(appID, "config", "launch")
        newEntryNumber = str(len(launchOptions))
        self.set_data_from_section(
            appID, {}, "config", "launch", newEntryNumber
        )

        self.update_launch_menu_window(appID)

    def split_directory(self, directory):
        allparts = []
        while True:
            parts = os.path.split(directory)
            if parts[0] == directory:
                allparts.insert(0, parts[0])
                break
            else:
                directory = parts[0]
                allparts.insert(0, parts[1])
        return allparts

    def calculate_parent_folders(self, executablePath, steamDir):
        # Splits all folders in the path into strings
        steamDir = self.split_directory(steamDir)
        execDir = self.split_directory(executablePath)

        if config.CURRENT_OS == "Windows":
            del steamDir[0]
            del execDir[0]

        while "" in steamDir:
            steamDir.remove("")
        while "" in execDir:
            execDir.remove("")

        parentFolders = None

        for index, folder in enumerate(steamDir):
            # Count how many folders are needed to reach the earliest common
            # parent folder
            if index == len(execDir) or folder != execDir[index]:
                parentFolders = len(steamDir) - index
                break

        if parentFolders is not None:
            return "../" * parentFolders + "/".join(execDir[index:])
        elif execDir[index:] == steamDir[index]:
            return ""
        else:
            return "/".join(execDir[index + 1:])

    def generate_launch_option_string(
        self, appID, execVar, wkngDirVar, pathType
    ):
        install_path = self.appinfo.parsedAppInfo[appID]["install_path"]

        if pathType == "exe":
            exePath = filedialog.askopenfilename(
                parent=self.launchMenuWindow, initialdir=install_path
            )
            if not exePath:
                return

            exePath = self.calculate_parent_folders(
                exePath, install_path
            )

            wkngDirPath = os.path.split(exePath)[0]

            if config.CURRENT_OS == "Windows":
                exePath = exePath.replace("/", "\\")
                wkngDirPath = wkngDirPath.replace("/", "\\")
            execVar.set(exePath)
            wkngDirVar.set(wkngDirPath)

        elif pathType == "wkngDir":
            wkngDirPath = filedialog.askdirectory(
                parent=self.launchMenuWindow, initialdir=install_path
            )
            if not wkngDirPath:
                return

            wkngDirPath = self.calculate_parent_folders(
                wkngDirPath, install_path
            )

            if config.CURRENT_OS == "Windows":
                wkngDirPath = wkngDirPath.replace("/", "\\")
            wkngDirVar.set(wkngDirPath)

    def write_os_list(self, appID, winVar, macVar, linVar, launchOption):
        oslist = []
        if winVar.get():
            oslist.append("windows")
        if macVar.get():
            oslist.append("macos")
        if linVar.get():
            oslist.append("linux")

        oslist = ",".join(oslist)

        self.set_data_from_section(
            appID, oslist, "config", "launch", launchOption, "config", "oslist"
        )

    def create_launch_option(
        self,
        frame,
        appID,
        number,
        description,
        executable,
        wkngDir,
        arguments,
        platforms,
    ):

        # Frames
        padding = 20
        mainFrame = LabelFrame(
            frame,
            padx=padding,
            pady=padding,
            text=number,
        )
        descFrame = Frame(mainFrame, padx=padding)
        execFrame = Frame(mainFrame, padx=padding)
        wkngDirFrame = Frame(mainFrame, padx=padding)
        argFrame = Frame(mainFrame, padx=padding)
        platformFrame = Frame(mainFrame, padx=padding)
        buttonsFrame = Frame(mainFrame, padx=padding)

        # String vars
        descVar = tk.StringVar()
        wkngDirVar = tk.StringVar()
        execVar = tk.StringVar()
        argVar = tk.StringVar()

        winVar = tk.BooleanVar()
        linVar = tk.BooleanVar()
        macVar = tk.BooleanVar()

        # Widgets
        descLabel = Label(descFrame, text="Description:")
        descEntry = Entry(
            descFrame,
            textvariable=descVar,
            width=60,
        )

        execLabel = Label(execFrame, text="Executable:")
        execEntry = Entry(
            execFrame,
            textvariable=execVar,
            width=55,
            state="readonly",
        )
        execButton = Button(
            execFrame,
            text="...",
            command=lambda: self.generate_launch_option_string(
                appID, execVar, wkngDirVar, "exe"
            ),
        )

        wkngDirLabel = Label(wkngDirFrame, text="Working Directory:")
        wkngDirEntry = Entry(
            wkngDirFrame,
            textvariable=wkngDirVar,
            width=55,
            state="readonly",
        )
        wkngDirButton = Button(
            wkngDirFrame,
            text="...",
            command=lambda: self.generate_launch_option_string(
                appID, execVar, wkngDirVar, "wkngDir"
            ),
        )

        argLabel = Label(argFrame, text="Launch Arguments:")
        argEntry = Entry(
            argFrame,
            textvariable=argVar,
            width=60,
        )

        # Platform checkbuttons
        winCheck = Checkbutton(
            platformFrame,
            text="Windows",
            variable=winVar,
        )
        linCheck = Checkbutton(
            platformFrame,
            text="Linux",
            variable=linVar,
        )
        macCheck = Checkbutton(
            platformFrame,
            text="Mac",
            variable=macVar,
        )

        deleteButton = DeleteButton(
            buttonsFrame,
            image=self.deleteImage,
            command=lambda: self.delete_launch_option(appID, number),
        )
        upButton = Button(
            buttonsFrame,
            image=self.upArrowImage,
            command=lambda: self.move_launch_option(appID, number, "up"),
        )
        downButton = Button(
            buttonsFrame,
            image=self.downArrowImage,
            command=lambda: self.move_launch_option(appID, number, "down"),
        )

        # Pack widgets
        descLabel.pack(side="left", fill="both")
        descEntry.pack(side="right", fill="both")

        wkngDirLabel.pack(side="left", fill="both")
        wkngDirButton.pack(side="right", fill="both")
        wkngDirEntry.pack(side="right", fill="both")

        execLabel.pack(side="left", fill="both")
        execButton.pack(side="right", fill="both")
        execEntry.pack(side="right", fill="both")

        argLabel.pack(side="left", fill="both")
        argEntry.pack(side="right", fill="both")

        winCheck.pack(side="left", fill="both")
        linCheck.pack(side="left", fill="both")
        macCheck.pack(side="left", fill="both")

        deleteButton.pack(side="right")
        downButton.pack(side="right")
        upButton.pack(side="right")

        # Pack frames
        mainFrame.pack(expand=True)
        descFrame.pack(side="top", fill="both", pady=(padding, 0))
        execFrame.pack(side="top", fill="both")
        wkngDirFrame.pack(side="top", fill="both")
        argFrame.pack(side="top", fill="both")
        platformFrame.pack(side="top")
        buttonsFrame.pack(side="top", fill="both", pady=(0, padding))

        # Insert data
        for platform in platforms.split(","):
            if platform == "windows":
                winVar.set(True)
            elif platform == "linux":
                linVar.set(True)
            elif platform == "macos":
                macVar.set(True)

        winVar.trace_add(
            "write",
            lambda _a, _b, _c: self.write_os_list(
                appID, winVar, macVar, linVar, number
            ),
        )
        linVar.trace_add(
            "write",
            lambda _a, _b, _c: self.write_os_list(
                appID, winVar, macVar, linVar, number
            ),
        )
        macVar.trace_add(
            "write",
            lambda _a, _b, _c: self.write_os_list(
                appID, winVar, macVar, linVar, number
            ),
        )

        self.set_var_no_callback(
            descVar,
            description,
            lambda _a, _b, _c: self.set_data_from_section(
                appID, descVar.get(), "config", "launch", number, "description"
            ),
        )

        self.set_var_no_callback(
            wkngDirVar,
            wkngDir,
            lambda _a, _b, _c: self.set_data_from_section(
                appID,
                wkngDirVar.get(),
                "config",
                "launch",
                number,
                "workingdir",
            ),
        )

        self.set_var_no_callback(
            execVar,
            executable,
            lambda _a, _b, _c: self.set_data_from_section(
                appID, execVar.get(), "config", "launch", number, "executable"
            ),
        )

        self.set_var_no_callback(
            argVar,
            arguments,
            lambda _a, _b, _c: self.set_data_from_section(
                appID, argVar.get(), "config", "launch", number, "arguments"
            ),
        )

        # Update to return correct values
        mainFrame.update()
        return [
            mainFrame.winfo_reqwidth() + padding,
            mainFrame.winfo_reqheight(),
            padding,
        ]

    def update_launch_menu_window(self, appID):
        # Clear frame and store current scroll position
        scrollbarPosition = 0
        for widget in self.scrollFrame.scrollableFrame.winfo_children():
            scrollbarPosition = self.scrollFrame.scrollbar.get()[0]
            widget.destroy()

        # Read launch options and gather data
        appLaunchOptions = self.get_data_from_section(
            appID, "config", "launch"
        )
        if not appLaunchOptions:
            self.ask_to_create_launch_option(appID)
            return

        frameCount = 0
        for launchOption in appLaunchOptions.keys():
            description = self.get_data_from_section(
                appID, "config", "launch", launchOption, "description"
            )
            executable = self.get_data_from_section(
                appID, "config", "launch", launchOption, "executable"
            )
            wkngDir = self.get_data_from_section(
                appID, "config", "launch", launchOption, "workingdir"
            )
            arguments = self.get_data_from_section(
                appID, "config", "launch", launchOption, "arguments"
            )
            platforms = self.get_data_from_section(
                appID,
                "config",
                "launch",
                launchOption,
                "config",
                "oslist",
                error="Not specified",
            )

            geometry = self.create_launch_option(
                self.scrollFrame.scrollableFrame,
                appID,
                launchOption,
                description,
                executable,
                wkngDir,
                arguments,
                platforms,
            )

            if frameCount < 2:
                frameCount += 1

        # Add widgets for adding new entries
        newEntryFrame = Frame(self.scrollFrame.scrollableFrame)
        newEntryButton = Button(
            newEntryFrame,
            text="Add New Entry",
            command=lambda: self.add_launch_option(appID),
        )

        padding = 10
        newEntryButton.pack(side="top", anchor="n")
        newEntryFrame.pack(side="bottom", pady=(padding, 0))

        # Offsets size of scrollbar and
        # takes padding (geometry[2]) into account
        self.scrollFrame.scrollbar.update()
        geometry[0] += self.scrollFrame.scrollbar.winfo_reqwidth()
        geometry[1] *= frameCount
        geometry[1] += geometry[2] * 2
        geometry[1] += newEntryFrame.winfo_reqheight() + padding

        # Resizes window depending on the number of launch options
        self.scrollFrame.canvas.config(width=geometry[0], height=geometry[1])
        self.scrollFrame.canvas.yview_moveto(scrollbarPosition)

    def create_launch_menu_window(self):
        appName = self.nameVar.get()
        appID = int(self.idVar.get())

        self.launchMenuWindow = tk.Toplevel(self.window)
        self.launchMenuWindow.resizable(False, False)
        self.launchMenuWindow.title(
            f"Launch Menu Editor for {appName} ({appID})"
        )

        self.scrollFrame = ScrollableFrame(self.launchMenuWindow)
        self.scrollFrame.scrollableFrame.config(bg=config.BG, padx=20, pady=20)

        self.update_launch_menu_window(appID)

        self.scrollFrame.pack()

        self.launchMenuWindow.update()
        self.center_window(self.launchMenuWindow)
        # Prevent the use of the main window while this one exists
        self.launchMenuWindow.grab_set()
        self.launchMenuWindow.mainloop()

    def populate_app_list(self):
        # Get all applications found in appinfo.vdf
        keys = list(self.appinfo.parsedAppInfo.keys())

        self.appData = []

        for app in keys[2:]:
            appID = app
            appType = self.get_data_from_section(appID, "common", "type")
            modified = appID in self.modifiedApps
            appName = self.get_data_from_section(appID, "common", "name")
            if not appName or not appType:
                pass
            else:
                self.appData.append([str(appName), appType, modified, appID])

        # Sort case-insensitive
        self.appData.sort(key=lambda x: str(x[0]).lower())

        for app in self.appData:
            self.insert_app_in_list(app)


class LoadingWindow(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Steam Metadata Editor (Loading)")
        self.resizable(width=False, height=False)
        self.config(bg=config.BG)

        self.loadingLabel = Label(self, text="Loading appinfo.vdf...")

        self.loadingLabel.pack(padx=30, pady=30)

        # Wait for widgets to actually load in
        # else they are sometimes not displayed,

        # TODO: Figure out why this hangs some systems
        # self.loadingLabel.wait_visibility()
        # self.wait_visibility()

        self.update()
