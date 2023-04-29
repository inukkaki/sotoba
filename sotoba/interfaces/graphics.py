import tkinter as tk


class Graphics:
    def __init__(self, canvas: tk.Canvas, scale: int) -> None:
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

    def set_visibility(self, item_id: int, is_visible: bool) -> None:
        mapping = {False: "hidden", True: "normal"}
        self.configure(item_id, state=mapping[is_visible])

    def locate(self, item_id: int, x: float, y: float,
               is_to_be_rounded_off: bool = True) -> None:
        if is_to_be_rounded_off:
            x0 = self.scale * int(x + 0.5)
            y0 = self.scale * int(y + 0.5)
        else:
            x0 = self.scale * x
            y0 = self.scale * y
        self.cvs.moveto(item_id, x0, y0)


class GraphicRect:
    def __init__(self, graphics: Graphics, x: float, y: float, width: float,
                 height: float, outline: str = "white",
                 fill: str | None = None, is_visible: bool = False) -> None:
        self.gfx = graphics
        self.item_id = self.gfx.add_rect(x, y, width, height, outline=outline,
                                         fill=fill)
        self.set_visibility(is_visible)

    def __del__(self) -> None:
        self.gfx.delete_item(self.item_id)

    def set_visibility(self, is_visible: bool) -> None:
        self.gfx.set_visibility(self.item_id, is_visible)

    def move_to(self, x: float, y: float) -> None:
        self.gfx.locate(self.item_id, x, y, is_to_be_rounded_off=False)
