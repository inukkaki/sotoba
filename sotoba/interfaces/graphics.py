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

    def add_text(self, x: float, y: float, text: str, anchor: str = "nw",
                 color: str = "white") -> int:
        if anchor != "center":
            if "s" in anchor:
                y0 = self.scale*(y + 1) - 1
            else:
                y0 = self.scale * y
            if "e" in anchor:
                x0 = self.scale*(x + 1) - 1
            else:
                x0 = self.scale * x
        else:
            x0 = self.scale * x
            y0 = self.scale * y
        item_id = self.cvs.create_text(x0, y0, text=text, anchor=anchor,
                                       fill=color)
        return item_id

    def delete_item(self, item_id: int) -> None:
        self.cvs.delete(item_id)

    def configure(self, item_id: int, **kwargs) -> None:
        self.cvs.itemconfigure(item_id, **kwargs)
