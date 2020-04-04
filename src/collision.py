import time
import pyglet
from .physics import PhysicalObject
from functools import total_ordering


@total_ordering
class Collision:
    def __init__(self, timestamp: float, obj1: PhysicalObject, obj2: PhysicalObject):
        self.next_ts = timestamp
        self.a = obj1
        self.b = obj2
        # save collision counts at the event time creation
        self.a_collisions = getattr(obj1, 'collisions', None)
        self.b_collisions = getattr(obj2, 'collisions', None)

    def __lt__(self, other):
        return self.next_ts < other.next_ts

    def __eq__(self, other):
        return self.next_ts == other.next_ts

    def is_valid(self):
        # if noting happened to the objects since the creation of the even the event is valid
        return (self.a_collisions == self.a.collisions if self.a else True) and \
               (self.b_collisions == self.b.collisions if self.b else True)

    def update(self, dt):
        if self.a:
            self.a.update(dt)
        if self.b:
            self.b.update(dt)

    def __call__(self, balls):
        """Handle the collision and predict future collisions for involved objects"""
        t = self.next_ts
        new_collisions = []
        if self.is_valid():
            if self.a and self.b:
                self.a.bounce_off(self.b)
                new_collisions.extend(self.a.predict(t, balls))
                new_collisions.extend(self.b.predict(t, balls))
            elif self.a:
                self.a.bounce_off_vertical_wall()
                new_collisions.extend(self.a.predict(t, balls))
            else:
                self.b.bounce_off_horizontal_wall()
                new_collisions.extend(self.b.predict(t, balls))
        return new_collisions

    def __str__(self):
        return f'{self.next_ts}: {self.a} - {self.b}'

