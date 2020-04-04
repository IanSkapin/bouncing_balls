import time
import pyglet
from .physics import PhysicalObject
from functools import total_ordering


@total_ordering
class Collision:
    def __init__(self, time: float, obj1: PhysicalObject, obj2: PhysicalObject, balls: list, pq: list):
        self.next_ts = time
        self.a = obj1
        self.b = obj2
        # save collision counts at the event time creation
        self.a_collisions = getattr(obj1, 'collisions', None)
        self.b_collisions = getattr(obj2, 'collisions', None)
        # list af all the objects
        self.balls = balls
        self.pq = pq

    def __lt__(self, other):
        return self.next_ts < other.next_ts

    def __eq__(self, other):
        return self.next_ts == other.next_ts

    def is_valid(self):
        # if noting happened to the objects since the creation of the even the event is valid
        return (self.a_collisions == self.a.collisions if self.a else True) and \
               (self.b_collisions == self.b.collisions if self.b else True)

    def __call__(self, dt, *args, **kwargs):
        """Get the next valid event and add it to the pyglet schedule, recalculate events for objects in the collision"""
        t = time.perf_counter()
        if self.is_valid():
            if self.a and self.b:
                self.a.bounce_off(self.b)
                self.a.predict(t, self.pq, self.balls)
                self.b.predict(t, self.pq, self.balls)
            elif self.a:
                self.a.bounce_off_vertical_wall()
                self.a.predict(t, self.pq, self.balls)
            else:
                self.b.bounce_off_horizontal_wall()
                self.b.predict(t, self.pq, self.balls)
        # get the next valid collision and push it on the pyglet schedule
        for _ in range(min(4, len(self.pq))):
            collision = pyglet.clock.heappop(self.pq)
            pyglet.clock.schedule_once(collision, collision.next_ts - time.perf_counter())

    def __str__(self):
        return f'{self.next_ts}: {self.a} - {self.b}'

