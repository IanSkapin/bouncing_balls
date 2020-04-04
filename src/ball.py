"""

"""
from pyglet.clock import heappush
from . import resources
from .physics import PhysicalObject, INFINITY
from .resources import black_ball_image
from .collision import Collision


class GhostBall(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(black_ball_image, *args, **kwargs)

    def update(self, dt):
        # collision with vertical wall
        if self.x + self.velocity_x * dt < self.radius or self.x + self.velocity_x * dt > resources.WIDTH - self.radius:
            self.velocity_x = -self.velocity_x
        # collision with horizontal wall
        if self.y + self.velocity_y * dt < self.radius or self.y + self.velocity_y * dt > resources.HEIGHT - self.radius:
            self.velocity_y = -self.velocity_y
        # new position
        super().update(dt)


class Ball(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(black_ball_image, *args, **kwargs)

    def time_to_hit_vertical_wall(self):
        """Return time prediction of a collision with vertical wall, or INFINITY"""
        if self.velocity_x < 0:
            return (self.radius - self.x) / self.velocity_x
        elif self.velocity_x > 0:
            return (resources.WIDTH - self.radius - self.x) / self.velocity_x
        return INFINITY

    def bounce_off_vertical_wall(self):
        """Handle collision with vertical wall"""
        self.collisions += 1
        self.velocity_x = -self.velocity_x

    def time_to_hit_horizontal_wall(self):
        """Return time prediction of a collision with vertical wall, or INFINITY"""
        if self.velocity_y < 0:
            return (self.radius - self.y) / self.velocity_y
        elif self.velocity_y > 0:
            return (resources.HEIGHT - self.radius - self.y) / self.velocity_y
        return INFINITY

    def bounce_off_horizontal_wall(self):
        """Handle collision with horizontal wall"""
        self.collisions += 1
        self.velocity_y = -self.velocity_y

    def predict(self, time: float, pq: list, balls: list):
        for ball in balls:
            if dt := self.time_to_hit(ball):
                heappush(pq, Collision(time=time + dt, obj1=self, obj2=ball, balls=balls, pq=pq))
        if dt := self.time_to_hit_vertical_wall():
            heappush(pq, Collision(time + dt,   obj1=self, obj2=None, balls=balls, pq=pq))
        if dt := self.time_to_hit_horizontal_wall():
            heappush(pq, Collision(time + dt, obj1=None, obj2=self, balls=balls, pq=pq))
