import pyglet

WIDTH = 800
HEIGHT = 600

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

black_ball_image = pyglet.resource.image("black_dot.png")


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


center_image(black_ball_image)

