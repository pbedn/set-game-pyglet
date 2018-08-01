import pyglet


COLORS = ['red', 'purple', 'green']
SHAPES = ['oval', 'squiggle', 'diamond']
NUMBERS = ['one', 'two', 'three']
SHADINGS = ['solid', 'striped', 'outlined']


class Card(pyglet.sprite.Sprite):
    def __init__(self, img, card_color, card_shape, card_pattern, card_number):
        super().__init__(img)
        self.colour = card_color
        self.shape = card_shape
        self.pattern = card_pattern
        self.number = card_number
        self.scale = 0.75

    def set_position(self, x, y):
        self.x = x
        self.y = y

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.frame_rate = 1/60.0

        self.cards = read_card_images()
    def on_draw(self):
        self.clear()

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = GameWindow(width=1024, height=600, caption="Sets", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
