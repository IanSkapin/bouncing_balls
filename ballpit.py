import sys
import time
import pyglet
import random
from src import resources
from src.ball import Ball


game_window = pyglet.window.Window(resources.WIDTH, resources.HEIGHT)
pyglet.gl.glClearColor(1, 1, 1, 1)

main_batch = pyglet.graphics.Batch()

balls = []


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    for o in balls:
        o.update(dt)


if __name__ == '__main__':
    next_collision = []

    # initialize all the balls
    for i in range(int(sys.argv[1])):
        balls.append(Ball(x=random.randint(50, resources.WIDTH - 50),
                          y=random.randint(50, resources.HEIGHT - 50),
                          velocity_x=(random.random() - 0.5) * int(sys.argv[2]),
                          velocity_y=(random.random() - 0.5) * int(sys.argv[2]),
                          batch=main_batch,
                          mass=random.random()))
    # initialize the priority queue
    t = time.perf_counter()
    for ball in balls:
        ball.predict(time=t, pq=next_collision, balls=balls)

    # schedule the first collision
    collision = pyglet.clock.heappop(next_collision)
    pyglet.clock.schedule_once(collision, collision.next_ts - t)

    # regular interval draws
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
