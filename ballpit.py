import sys
import time
import pyglet
import random
import heapq
from src import resources
from src.ball import Ball


game_window = pyglet.window.Window(resources.WIDTH, resources.HEIGHT)
pyglet.gl.glClearColor(1, 1, 1, 1)

main_batch = pyglet.graphics.Batch()


class TimeElapsed:
    def __init__(self):
        self.t = 0

    def new_dt(self, dt):
        previous = self.t
        self.t += dt
        return previous, self.t


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt, pq, t):
    """Resolve objects that were suppose to collide in this interval first by:
     - updating their position to the collision point, then
     - handle the collision, and finally
     - update their position to match the dt
     Update all the objects not involved in collisions as well.
    """
    ta, tb = t.new_dt(dt)
    while pq and pq[0].next_ts < tb:
        collision = heapq.heappop(pq)
        if not collision.is_valid():
            continue
        dt_a = collision.next_ts - ta
        for o in balls:
            o.update(dt_a)
        [heapq.heappush(pq, col) for col in collision(balls=balls)]
        ta += dt_a

    for o in balls:
        o.update(tb - ta)


if __name__ == '__main__':
    pq = []
    balls = []
    # initialize all the balls
    for i in range(int(sys.argv[1])):
        balls.append(Ball(x=random.randint(10, resources.WIDTH - 10),
                          y=random.randint(10, resources.HEIGHT - 0),
                          velocity_x=random.random() - 0.5,
                          velocity_y=random.random() - 0.5,
                          batch=main_batch,
                          mass=random.random()))
    balls.append(Ball(x=100, y=100,
                      velocity_y=int(sys.argv[2]), velocity_x=int(sys.argv[2]),
                      batch=main_batch, mass=4))
    # initialize the priority queue
    for ball in balls:
        [heapq.heappush(pq, col) for col in ball.predict(time=0, balls=balls)]

    t = TimeElapsed()
    # regular interval draws
    pyglet.clock.schedule_interval(update, 1/60.0, pq=pq, t=t)
    pyglet.app.run()
