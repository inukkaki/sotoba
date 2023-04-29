from sotoba.interfaces.graphics import GraphicRect, Graphics
from sotoba.models.fundamentals import Vector


class Entity:
    WIDTH = 0
    HEIGHT = 0

    WEIGHT = 1.0

    def __init__(self, x: float = 0.0, y: float = 0.0, vx: float = 0.0,
                 vy: float = 0.0, ax: float = 0.0, ay: float = 0.0) -> None:
        self.r = Vector(x, y)
        self.v = Vector(vx, vy)
        self.a = Vector(ax, ay)

        # CONservative and NON-conservative forces
        self.f = {"con": Vector(0.0, 0.0), "non": Vector(0.0, 0.0)}
        self.force_requests = {"con": [], "non": []}

        self.weight = self.WEIGHT

    def behave(self, **kwargs) -> None:
        pass

    def update(self, **kwargs) -> None:
        self.behave(**kwargs)

    def add_forces(self) -> None:
        for kind_of_forces in self.force_requests:
            force_list = self.force_requests[kind_of_forces]
            self.f[kind_of_forces].assign(0.0, 0.0)
            for force in force_list:
                self.f[kind_of_forces] += force
            force_list.clear()

    def accelerate(self) -> None:
        self.a.assign(0.0, 0.0)
        self.a += (self.f["con"] + self.f["non"]) / self.weight
        self.v += self.a

    def move(self) -> None:
        self.r += self.v

    @property
    def info(self) -> dict:
        product = {
            "position": {
                "x": self.r.x, "y": self.r.y, "vx": self.v.x, "vy": self.v.y,
                "ax": self.a.x, "ay": self.a.y
            }
        }
        return product


class PlayableEntity(Entity):
    WIDTH = 14
    HEIGHT = 16

    WEIGHT = 5.0

    def __init__(self, graphics: Graphics, x: float = 0.0, y: float = 0.0,
                 vx: float = 0.0, vy: float = 0.0, ax: float = 0.0,
                 ay: float = 0.0) -> None:
        super().__init__(x, y, vx, vy, ax, ay)
        self.key_bind = {"walk": {"left": 37, "right": 39}}

        # [!] just for debugging
        self.rect = GraphicRect(graphics, self.r.x, self.r.y, self.WIDTH,
                                self.HEIGHT, is_visible=True)

    def behave(self, **kwargs) -> None:
        self.operate(kwargs["detected_keys"])

        self.add_forces()
        self.accelerate()
        self.move()

        # [!] just for debugging
        self.rect.move_to(self.r.x, self.r.y)

    def operate(self, detected_keys: dict[str, set]) -> None:
        key_bind_walk = self.key_bind["walk"]
        if not set(key_bind_walk.values()) <= detected_keys["remaining"]:
            force = Vector(0.0, 0.0)
            if key_bind_walk["left"] in detected_keys["remaining"]:
                force.assign(-0.25, 0.0)
            elif key_bind_walk["right"] in detected_keys["remaining"]:
                force.assign(0.25, 0.0)
            self.force_requests["non"].append(force)
