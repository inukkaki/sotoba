import tkinter as tk

from sotoba.interfaces.control import Controller
from sotoba.interfaces.graphics import Graphics


TITLE = "sotoba"

WINDOW_WIDTH = 352
WINDOW_HEIGHT = 240


# Resolve the blurriness of the window (Windows 10)
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    pass


class Window:
    def __init__(self, root: tk.Tk, scale: float = 2.0) -> None:
        self.root = root
        self.root.title(TITLE)
        self.root.resizable(width=False, height=False)

        self.scale = ...
        self.width = ...
        self.height = ...
        self.resize(scale, WINDOW_WIDTH, WINDOW_HEIGHT)

        canvas_width = int(self.scale * self.width)
        canvas_height = int(self.scale * self.height)
        canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height,
                           bg="black", borderwidth=0, highlightthickness=0)
        canvas.grid(column=0, row=0, sticky=("n", "w", "e", "s"))
        self.gfx = Graphics(canvas, self.scale)

        self.controller = Controller(self.root, self.gfx)

    def resize(self, scale: float, width: int, height: int) -> None:
        self.scale = scale
        self.width = width
        self.height = height

        new_width = int(self.scale * self.width)
        new_height = int(self.scale * self.height)
        x = (self.root.winfo_screenwidth() - new_width) // 2
        y = (self.root.winfo_screenheight() - new_height) // 2
        new_geometry = f"{new_width}x{new_height}+{x}+{y}"

        self.root.geometry(new_geometry)
