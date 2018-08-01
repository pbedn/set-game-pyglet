import random
from collections import namedtuple

import pyglet
from pyglet.window import mouse, key


COLORS = ['red', 'purple', 'green']
SHAPES = ['oval', 'diamond', 'squiggle']
NUMBERS = ['one', 'two', 'three']
SHADINGS = ['solid', 'striped', 'outlined']

# coordinates [x, y, right: x + width, top: y + height] of image on viewport
Box = namedtuple("Box", "x y right top")


class Card(pyglet.sprite.Sprite):
    """
    Single Card sprite object
    """
    def __init__(self, img, card_color, card_shape, card_pattern, card_number):
        super().__init__(img)
        self.colour = card_color
        self.shape = card_shape
        self.pattern = card_pattern
        self.number = card_number
        self.scale = 0.75

        self.box = Box(5000, 5000, 100, 100)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.box = Box(self.x, self.y, self.x+self.width, self.y+self.height)

    def is_in_the_box(self, x, y):
        if self.box.x <= x <= self.box.right \
                and self.box.y <= y <= self.box.top:
            return True

    def __str__(self):
        return "Card: {}, {}, {}, {}".format(self.colour, self.shape, self.pattern, self.number)


def read_card_images():
    red_deck = pyglet.image.load('res/sets-red.png')
    green_deck = pyglet.image.load('res/sets-green.png')
    purple_deck = pyglet.image.load('res/sets-purple.png')
    red_deck_seq = pyglet.image.ImageGrid(red_deck, 9, 3)
    green_deck_seq = pyglet.image.ImageGrid(green_deck, 9, 3)
    purple_deck_seq = pyglet.image.ImageGrid(purple_deck, 9, 3)

    seq = {'red': red_deck_seq, 'green': green_deck_seq, 'purple': purple_deck_seq}

    card_list = []

    for color, s in seq.items():
        card_seq = iter(reversed(s))

        for pattern in SHADINGS:
            for shape in SHAPES:
                for number in NUMBERS:
                    card = card_seq.__next__()
                    card_list.append(Card(card, color, shape, pattern, number))

    return card_list


class GameWindow(pyglet.window.Window):
    """
    Game Director managing all actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.frame_rate = 1/60.0

        self.batch = pyglet.graphics.Batch()

        self.cards = read_card_images()
        self.cards_used = []

        # self.draw_selected('red', 'oval', 'solid', 'one', 50, 50)

        self.draw_random(4)
        self.draw_random(4, 250)
        self.draw_random(4, 500)
        self.draw_random(4, 750)

    def draw_selected(self, color, shape, pattern, number, x, y):
        for card in self.cards:
            if card.shape == shape and card.pattern == pattern \
                    and card.number == number and card.colour == color:
                card.set_position(x, y)
                card.batch = self.batch

    def draw_random(self, count, x=0):
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        for i, card in enumerate(cards):
            if i >= count:
                break
            self.draw_selected(card.colour, card.shape, card.pattern, card.number, x+50, 150*i)
            self.cards_used.append(card)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            for card in self.cards:
                if card.is_in_the_box(x, y):
                    print(card)
    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = GameWindow(width=1024, height=600, caption="Sets", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
