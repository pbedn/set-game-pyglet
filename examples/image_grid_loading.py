"""
How pyglet splits image into a grid ?
"""

import pyglet

window = pyglet.window.Window(resizable=True)

batch = pyglet.graphics.Batch()

pyglet.resource.path = ['../res']
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


seq = read_image('new-sets.png', 9, 9, center=True)
sprites = create_sprites(seq)


@window.event
def on_draw():
    window.clear()
    sprites[0].x = 50
    sprites[0].y = 50
    sprites[0].draw()

    sprites[1].x = 250
    sprites[1].y = 50
    sprites[1].draw()

    sprites[9].x = 50
    sprites[9].y = 200
    sprites[9].draw()

    sprites[10].x = 250
    sprites[10].y = 200
    sprites[10].draw()

    sprites[79].x = 450
    sprites[79].y = 50
    sprites[79].draw()

    sprites[80].x = 450
    sprites[80].y = 200
    sprites[80].draw()


pyglet.app.run()
