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

import re
import os
import platform
from argparse import ArgumentParser
from configparser import ConfigParser, ParsingError

from utils import ask_steam_path


class Config:
    def __init__(self):
        self.set_default_variables()

        self.parse_arguments()
        self.ensure_config_file_exists()

        self.config_parser = ConfigParser()
        try:
            self.config_parser.read(f"{self.CONFIG_PATH}/config.cfg")
        except ParsingError:
            self.create_new_config_file()

        self.STEAM_PATH = self.get_steam_path()

    def set_default_variables(self):
        # Looks for "path"		"/some/path"
        self.PATH_REGEX = re.compile('"path"\t\t"(.*)"')
        # Looks for "0213123"		"1395050123"
        self.APP_REGEX = re.compile('"([0-9]+)"\t\t"[0-9]+"')

        self.BG = "#23272c"
        self.FG = "#b8b6b4"

        self.ENTRY_FG = "#e9e9e9"
        self.ENTRY_BG = "#1d1b19"
        self.ENTRY_RELIEF = "flat"
        self.ENTRY_PADDING = 5

        self.BTTN_ACTIVE_BG = "#3ea7f3"
        self.BTTN_ACTIVE_FG = "#c3e1f8"
        self.BTTN_BG = "#2f7dde"
        self.BTTN_FG = "#c3e1f8"
        self.BTTN_RELIEF = "flat"
        self.BTTN_FONT_SIZE = 9
        self.BTTN_FONT = "Verdana"

        self.DLT_BTTN_BG = "#c44848"
        self.DLT_BTTN_ACTIVE_BG = "#c46565"

        self.FONT = "Verdana"

        self.CURRENT_OS = platform.system()

        self.HOME_DIR = None
        self.CONFIG_PATH = "config"
        self.IMG_PATH = f"{os.path.dirname(__file__)}/gui/img"

        if self.CURRENT_OS != "Windows":
            self.HOME_DIR = os.getenv("HOME")
            self.CONFIG_PATH = (
                f"{self.HOME_DIR}/.local/share/Steam-Metadata-Editor/config"
            )

        self.DEFAULT_STEAM_PATHS = {
            "Windows": "C:\\Program Files (x86)\\Steam",
            "Linux": f"{self.HOME_DIR}/.local/share/Steam",
            "Darwin": f"{self.HOME_DIR}/Library/Application Support/Steam",
        }

    def parse_arguments(self):
        parser = ArgumentParser()
        parser.add_argument(
            "-s",
            "--silent",
            action="store_true",
            help="silently patch appinfo.vdf with previously made modifications",
        )
        parser.add_argument(
            "-e",
            "--export",
            nargs="+",
            type=int,
            help="export the contents of all the given appIDs into the JSON",
        )
        args = parser.parse_args()
        self.silent = args.silent
        self.export = args.export

    def ensure_config_file_exists(self):
        if not os.path.isfile(f"{self.CONFIG_PATH}/config.cfg"):
            self.create_new_config_file()

    def create_new_config_file(self):
        os.makedirs(self.CONFIG_PATH, exist_ok=True)
        with open(f"{self.CONFIG_PATH}/config.cfg", "w"):
            pass

    def save_steam_path(self, steam_path):
        self.config_parser.add_section("STEAMPATH")
        self.config_parser.set("STEAMPATH", "Path", steam_path)
        with open(f"{self.CONFIG_PATH}/config.cfg", "w") as cfg:
            self.config_parser.write(cfg)

    def get_steam_path(self):
        if "STEAMPATH" in self.config_parser:
            steam_path = self.config_parser.get("STEAMPATH", "Path")
            if self.verify_steam_path(steam_path):
                return steam_path

        steam_path = self.DEFAULT_STEAM_PATHS.get(self.CURRENT_OS)
        while not self.verify_steam_path(steam_path):
            steam_path = ask_steam_path()
            if not steam_path:
                os._exit(0)

        self.save_steam_path(steam_path)

        return steam_path

    def verify_steam_path(self, steam_path):
        if not steam_path:
            return False
        appinfo_location = os.path.join(steam_path, "appcache", "appinfo.vdf")
        return os.path.isfile(appinfo_location)


config = Config()
