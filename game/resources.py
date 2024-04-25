import pyglet


def read_images_from_disk() -> pyglet.image.ImageGrid:
    """Read images from disk into sequence, grid and texture.

    :return: ImageGrid
    """
    deck = pyglet.resource.image("spritesheet.png")
    return pyglet.image.ImageGrid(deck, 9, 9)
