#!/usr/bin/env python3
#
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
#
##################################
#                                #
#       Created by tralph3       #
#   https://github.com/tralph3   #
#                                #
##################################

from tkinter import messagebox

from config import config
from gui.main_window import MainWindow
from appinfo import IncompatibleVDFError


def main():
    try:
        main_window = MainWindow()
        if not config.silent and config.export is None:
            main_window.window.mainloop()
    except IncompatibleVDFError as e:
        messagebox.showerror(
            title="Invalid VDF Version",
            message=f"VDF version {e.vdf_version:#08x} is not supported.",
        )


if __name__ == "__main__":
    main()
