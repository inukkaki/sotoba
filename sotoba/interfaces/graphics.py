import tkinter as tk


class Graphics:
    def __init__(self, canvas: tk.Canvas, scale: float) -> None:
        self.cvs = canvas
        self.scale = scale

    def add_rect(self, x: float, y: float, width: float, height: float,
                 outline: str = "white", fill: str | None = None) -> int:
        x0 = self.scale * x
        y0 = self.scale * y
        x1 = self.scale*(x + width) - 1
        y1 = self.scale*(y + height) - 1
        item_id = self.cvs.create_rectangle(x0, y0, x1, y1, outline=outline,
                                            fill=fill)
        return item_id
