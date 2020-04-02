import sys
import pyglet
import random
from src import resources
from src.ball import GhostBall as Ball


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

    for i in range(int(sys.argv[1])):
        balls.append(Ball(x=random.randint(0, resources.WIDTH),
                          y=random.randint(0, resources.HEIGHT),
                          velocity_x=(random.random() - 0.5) * int(sys.argv[2]),
                          velocity_y=(random.random() - 0.5) * int(sys.argv[2]),
                          batch=main_batch,
                          mass=random.random()))

    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
