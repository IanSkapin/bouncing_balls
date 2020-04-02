"""

"""
from . import resources
from .physics import PhysicalObject
from .resources import black_ball_image


class Ball:
    pass


class GhostBall(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(black_ball_image, *args, **kwargs)

    def update(self, dt):
        if self.x + self.velocity_x * dt < self.radius or self.x + self.velocity_x * dt > resources.WIDTH - self.radius:
            self.velocity_x = -self.velocity_x
        if self.y + self.velocity_y * dt < self.radius or self.y + self.velocity_y * dt > resources.HEIGHT - self.radius:
            self.velocity_y = -self.velocity_y
        super().update(dt)

