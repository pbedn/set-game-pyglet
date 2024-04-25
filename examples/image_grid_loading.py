"""How pyglet splits image into a grid ?
"""
from __future__ import annotations

import pyglet
from pyglet.shapes import Box

window = pyglet.window.Window(resizable=True)

batch = pyglet.graphics.Batch()

pyglet.resource.path = ["."]
pyglet.resource.reindex()


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def read_image(image, rows, columns, center=False):
    deck = pyglet.resource.image(image)
    center_image(deck) if center else None
    deck_seq = pyglet.image.ImageGrid(deck, rows=rows, columns=columns, row_padding=10, column_padding=9)
    return deck_seq


def create_sprites(seq):
    sprite_list = []
    for i, image in enumerate(seq):
        sprite = pyglet.sprite.Sprite(image, batch=batch)
        sprite.scale = 2
        sprite_list.append(sprite)
    return sprite_list


seq = read_image("new-sets.png", 9, 9, center=True)
sprites = create_sprites(seq)

s = sprites[0]
rectangle = Box(s.x, s.y, s.width, s.height, color=(255, 255, 0), batch=batch)
rectangle.opacity = 128
rectangle.rotation = 0


@window.event
def on_draw():
    window.clear()
    rectangle.draw()

    sprites[80].x = 450
    sprites[80].y = 200
    sprites[80].draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if rectangle.x < x < rectangle.x + rectangle.width and rectangle.y < y < rectangle.y + rectangle.width:
        print(x, y)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if rectangle.x < x < rectangle.x + rectangle.width and rectangle.y < y < rectangle.y + rectangle.width:
        rectangle.x += dx
        rectangle.y += dy


pyglet.app.run()
