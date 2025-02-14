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

from tkinter import filedialog, messagebox


def ask_steam_path():
    messagebox.showinfo(
        title="Can't locate Steam",
        message="Steam couldn't be located in your system, "
        + "or there's no \"appinfo.vdf\" file present. "
        + "Please point to it's installation directory."
    )
    return filedialog.askdirectory()
