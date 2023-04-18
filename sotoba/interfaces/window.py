import tkinter as tk


# Resolve the blurriness of the window (Windows 10)
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    pass


class Window:
    def __init__(self, root: tk.Tk, scale: float = 2.0) -> None:
        self.root = root
        self.root.title("sotoba")

        self.scale = ...
        self.width = ...
        self.height = ...
        self.resize(scale, 352, 240)

    def resize(self, scale: float, width: int, height: int) -> None:
        self.scale = scale
        self.width = int(self.scale * width)
        self.height = int(self.scale * height)

        x = (self.root.winfo_screenwidth() - self.width) // 2
        y = (self.root.winfo_screenheight() - self.height) // 2
        new_geometry = f"{self.width}x{self.height}+{x}+{y}"

        self.root.geometry(new_geometry)
