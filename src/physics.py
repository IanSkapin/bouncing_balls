import math

import pyglet

INFINITY = -1


class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        self.velocity_x = kwargs.pop('velocity_x', 0.0)
        self.velocity_y = kwargs.pop('velocity_y', 0.0)
        self.mass = kwargs.pop('mass', 0)
        super().__init__(*args, **kwargs)
        self.event_handlers = []
        self.collisions = 0

    @property
    def radius(self):
        return (self.image.width * self.scale) / 2

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def time_to_hit(self, other):
        if self == other:
            return INFINITY
        dx = other.x - self.x
        dy = other.y - self.y

        dvx = other.velocity_x - self.velocity_x
        dvy = other.velocity_y - self.velocity_y
        dvdr = dx * dvx + dy * dvy
        if dvdr > 0:
            return INFINITY

        dvdv = dvx * dvx + dvy * dvy
        drdr = dx * dx + dy * dy
        sigma = self.radius + other.radius
        d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma)
        if d < 0:
            return INFINITY
        return -(dvdr + math.sqrt(d)) / dvdv

    def bounce_off(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dvx = other.velocity_x - self.velocity_x
        dvy = other.velocity_y - self.velocity_y
        dvdr = dx * dvx + dy * dvy
        dist = self.radius + other.radius
        j = 2 * self.mass * other.mass * dvdr / ((self.mass + other.mass) * dist)
        jx = j * dx / dist
        jy = j * dy / dist

        self.velocity_x += jx / self.mass
        self.velocity_y += jy / self.mass

        other.velocity_x -= jx / other.mass
        other.velocity_y -= jy / other.mass

        self.collisions += 1
        other.collisions += 1


