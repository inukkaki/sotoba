from sotoba.interfaces.graphics import GraphicRect, Graphics


class Playable:
    WIDTH = 14
    HEIGHT = 16

    def __init__(self, graphics: Graphics, x: float, y: float) -> None:
        self.width = self.WIDTH
        self.height = self.HEIGHT

        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        self.rect = GraphicRect(graphics, self.x, self.y, self.width,
                                self.height, is_visible=True)

    def operate(self, detected_keys: dict[str, set]) -> None:
        # Walking
        if {37, 39} <= detected_keys["remaining"]:
            self.ax = 0
        else:
            if 37 in detected_keys["remaining"]:
                self.ax = -0.05
            if 39 in detected_keys["remaining"]:
                self.ax = 0.05

        self.calculate()

    def calculate(self) -> None:
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy

        self.ax = 0
        self.ay = 0

        self.rect.move_to(self.x, self.y)
