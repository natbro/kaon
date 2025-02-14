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

import tkinter as tk

from config import config


class Frame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=config.BG, **kwargs)


class LabelFrame(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=config.BG, fg=config.FG, font=config.FONT, **kwargs)


class Label(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=config.BG, fg=config.FG, font=config.FONT, **kwargs)


class Scrollbar(tk.Scrollbar):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            bd=0,
            relief=config.ENTRY_RELIEF,
            bg=config.ENTRY_BG,
            activebackground=config.ENTRY_BG,
            **kwargs
        )


class Checkbutton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            bg=config.BG,
            fg=config.ENTRY_FG,
            relief=config.ENTRY_RELIEF,
            selectcolor=config.ENTRY_BG,
            **kwargs
        )


class Entry(tk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            font=config.FONT,
            readonlybackground=config.ENTRY_BG,
            relief=config.ENTRY_RELIEF,
            bg=config.ENTRY_BG,
            fg=config.ENTRY_FG,
            **kwargs
        )


class Button(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            activebackground=config.BTTN_ACTIVE_BG,
            activeforeground=config.BTTN_ACTIVE_FG,
            relief=config.BTTN_RELIEF,
            font=(config.BTTN_FONT, config.BTTN_FONT_SIZE),
            bg=config.BTTN_BG,
            fg=config.BTTN_FG,
            **kwargs
        )


class DeleteButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            activebackground=config.DLT_BTTN_ACTIVE_BG,
            activeforeground=config.BTTN_ACTIVE_FG,
            relief=config.BTTN_RELIEF,
            font=(config.BTTN_FONT, config.BTTN_FONT_SIZE),
            bg=config.DLT_BTTN_BG,
            fg=config.BTTN_FG,
            **kwargs
        )


class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.scrollableFrame = Frame(self.canvas)

        self.scrollableFrame.bind(
            "<Configure>",
            lambda _e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas.create_window(
            (0, 0), window=self.scrollableFrame, anchor="nw"
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # X11
        self.canvas.bind_all("<Button-4>", self.scroll_canvas)
        self.canvas.bind_all("<Button-5>", self.scroll_canvas)
        # Everything else
        self.canvas.bind_all("<MouseWheel>", self.scroll_canvas)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def scroll_canvas(self, event):
        if event.num == 5 or event.delta < 0:
            direction = 1
        elif event.num == 4 or event.delta > 0:
            direction = -1

        self.canvas.yview_scroll(direction, "units")
