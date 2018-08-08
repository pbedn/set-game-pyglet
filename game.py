import random
from itertools import combinations
from collections import namedtuple

import pyglet
from pyglet.window import mouse, key


COLORS = ['red', 'purple', 'green']
SHAPES = ['oval', 'diamond', 'squiggle']
NUMBERS = ['one', 'two', 'three']
PATTERNS = ['solid', 'striped', 'outlined']
FEATURES = {'color_name': COLORS, 'shape': SHAPES, 'number': NUMBERS, 'pattern': PATTERNS}

# coordinates [x, y, right: x + width, top: y + height] of card image on viewport
Box = namedtuple("Box", "x y right top")

SCALE_CARD_SELECTED = 0.80
SCALE_CARD_UNSELECTED = 0.70

MENU_TEXT_FEATURES_QUICKSTART = "Quickstart: 3 features"
MENU_TEXT_FEATURES_NORMAL = "Normal: 4 features"
FEATURES_QUICKSTART = 'quickstart'
FEATURES_NORMAL = 'normal'


class Card(pyglet.sprite.Sprite):
    """
    Single Card sprite object
    """
    def __init__(self, img, card_color, card_shape, card_pattern, card_number):
        super().__init__(img)
        self.color_name = card_color
        self.shape = card_shape
        self.pattern = card_pattern
        self.number = card_number
        self.scale = SCALE_CARD_UNSELECTED
        self.scale_x = 0.9

        # Coordinates of box at init are out of real window
        self.box = Box(5000, 5000, 100, 100)

    def set_position(self, x, y):
        """
        Set position of sprite in window and create box variable

        :param x:
        :param y:
        """
        self.x = x
        self.y = y
        self.box = Box(self.x, self.y, self.x+self.width, self.y+self.height)

    def is_in_the_box(self, x, y):
        """
        Check if point (x,y) is inside card box (rectangle)

        :param x:
        :param y:
        :return: True if point (x,y) is inside box
        """
        if self.box.x <= x <= self.box.right \
                and self.box.y <= y <= self.box.top:
            return True

    def __str__(self):
        return "Card: {}, {}, {}, {}".format(self.color_name, self.shape, self.pattern, self.number)


def select_features(func, switch):
    """
    Remove selected feature from total cards list

    :param func: function reading images from resources
    :param switch: namedtuple with boolean features
    :return: List of cards after removal selected feature
    """
    cards = func()
    new_cards = cards.copy()

    def remove_cards(attribute, features, lst):
        if not getattr(switch, attribute):
            single_feat = random.choice(features)
            for card in cards:
                if getattr(card, attribute) != single_feat:
                    try:
                        lst.remove(card)
                    except ValueError:
                        pass

    for k, v in FEATURES.items():
        remove_cards(k, v, new_cards)

    return new_cards


def read_card_images():
    """
    Read images from disk into sequence and grid into one list

    :return: List containing all cards read from image resources
    """
    red_deck = pyglet.image.load('res/sets-red.png')
    green_deck = pyglet.image.load('res/sets-green.png')
    purple_deck = pyglet.image.load('res/sets-purple.png')
    red_deck_seq = pyglet.image.ImageGrid(red_deck, 9, 3, row_padding=2)
    green_deck_seq = pyglet.image.ImageGrid(green_deck, 9, 3, row_padding=2)
    purple_deck_seq = pyglet.image.ImageGrid(purple_deck, 9, 3, row_padding=2)

    seq = {'red': red_deck_seq, 'green': green_deck_seq, 'purple': purple_deck_seq}

    card_list = []
    for color, s in seq.items():
        card_seq = iter(reversed(s))
        for pattern in PATTERNS:
            for shape in SHAPES:
                for number in NUMBERS:
                    card = card_seq.__next__()
                    card_list.append(Card(card, color, shape, pattern, number))
    return card_list


class TextBase(pyglet.text.Label):
    """
    Display text on the screen
    """
    def __init__(self, x, y, text, batch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_name = 'Arial'
        self.font_size = 30
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.batch = batch
        self.text = text
        self.x = x
        self.y = y


class TextCountable(TextBase):
    def __init__(self, x, y, _text, batch, *args, **kwargs):
        super().__init__(x, y, _text, batch, *args, **kwargs)
        self._text = _text
        self._count = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        self.text = self._text + str(self._count)


class Cards:
    """
    Manager of all cards that are displayed on the screen

    and generated but hidden for the user
    """
    def __init__(self, rows, cols, feat_switch, batch):
        self.rows = rows
        self.cols = cols
        self.batch = batch

        self.cards = select_features(read_card_images, feat_switch)
        self._check_cards_number(feat_switch)

        self.cards_used = []
        self.card_clicked = []

        for i in range(self.cols):
            self.draw_random(i*200)

    def _check_cards_number(self, feat_switch):
        """
        Assert that number of cards after feature removal is correct
        All four features should have 81 cards
        Quickstart game (one feature off) - 27 cards

        :param feat_switch:
        """
        total = 81
        for attribute in FEATURES.keys():
            if not getattr(feat_switch, attribute):
                total /= 3
        assert len(self.cards) == total, "Number of cards after features removal is wrong"

    def __iter__(self):
        for card in self.cards:
            yield card

    def draw_selected(self, color, shape, pattern, number, x, y):
        """
        Set attributes and add to batch a selected card

        :param color:
        :param shape:
        :param pattern:
        :param number:
        :param x:
        :param y:
        """
        for card in self.cards:
            if card.shape == shape and card.pattern == pattern \
                    and card.number == number and card.color_name == color:
                card.set_position(x, y)
                card.batch = self.batch

    def draw_random(self, x):
        """
        Draw one column of random cards

        :param x: position offset of first drawn card
        """
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        for i, card in enumerate(cards):
            if i >= self.rows:
                break
            self.draw_selected(card.color_name, card.shape, card.pattern, card.number, x+25, 150*i+100)
            self.cards_used.append(card)

    def draw_single_random(self, x, y):
        """
        Draw single random card at given coordinates

        :param x:
        :param y:
        """
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        card = cards[0]
        self.draw_selected(card.color_name, card.shape, card.pattern, card.number, x, y)
        self.cards_used.append(card)

    @staticmethod
    def check_if_cards_are_set(cards_list):
        """
        Detailed conditions for correct set are described in README.
        If set consists of one or three elements then it is correct
        according to game rules, therefore it has to be different than 2

        :param cards_list:
        :return: True if cards in a list are set, False otherwise
        """
        assert len(cards_list) == 3
        result = True
        for attribute in FEATURES.keys():
            set_a = {getattr(cards_list[0], attribute),
                     getattr(cards_list[1], attribute),
                     getattr(cards_list[2], attribute)}
            result = result and len(set_a) != 2
        return result

    def check_if_set_exists_in_cards_used(self):
        """
        Iterate through all cards drawn on screen
        make combinations of three cards from them
        And check if they are a set

        :return: True if set exists among cards, False otherwise
        """
        result = []
        for c in combinations(self.cards_used, 3):
            result.append(self.check_if_cards_are_set(c))
        return True if True in result else False

    def number_of_cards_left(self):
        """
        Number of cards that are not draw on the screen
        :return: number o cards left if it is greater than zero, and zero otherwise
        """
        num = len(self.cards) - len(self.cards_used)
        return num if num >= 0 else 0


class Menu:
    def __init__(self, director):
        self.director = director

    def menu_init(self):
        start_game_menu_item = TextBase(self.director.width // 2, self.director.height // 2 + 100, "Start Game", batch=self.director.batch)
        start_game_menu_item.bold = True
        start_game_menu_item.font_size += 10
        features_menu_item = TextBase(self.director.width // 2, self.director.height // 2, MENU_TEXT_FEATURES_QUICKSTART, batch=self.director.batch)
        end_game_menu_item = TextBase(self.director.width // 2, self.director.height // 2 - 100, "Exit", batch=self.director.batch)
        self.menu_items = [start_game_menu_item, features_menu_item, end_game_menu_item]
        self.current_index = 0
        self.current_selection = self.menu_items[0]
        self.set_feature = FEATURES_QUICKSTART  # used to save number of features user (3 or 4) for cards init

        help = """
        Menu: Quickstart or Normal
        R - Restart during gameplay with previous settings
        F10 - Go to menu
        ESCAPE - Exit app
        """
        help_menu_item = TextBase(self.director.width // 2,
                                  self.director.height // 8,
                                  help,
                                  batch=self.director.batch,
                                  multiline=True,
                                  width=self.director.width)
        help_menu_item.font_size -= 18
        self.menu_items.append(help_menu_item)

    def choose_menu_item(self, symbol):
        if symbol == key.DOWN:
            self.current_selection.bold = False
            self.current_selection.font_size -= 10
            self.current_index += 1
            if self.current_index > 2:
                self.current_index = 0
            self.current_selection = self.menu_items[self.current_index]
            self.current_selection.bold = True
            self.current_selection.font_size += 10
        elif symbol == key.UP:
            self.current_selection.bold = False
            self.current_selection.font_size -= 10
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = 2
            self.current_selection = self.menu_items[self.current_index]
            self.current_selection.bold = True
            self.current_selection.font_size += 10
        elif self.current_index == 1 and symbol == key.RIGHT:
            self.set_feature = FEATURES_NORMAL
            self.current_selection.text = MENU_TEXT_FEATURES_NORMAL
        elif self.current_index == 1 and symbol == key.LEFT:
            self.set_feature = FEATURES_QUICKSTART
            self.current_selection.text = MENU_TEXT_FEATURES_QUICKSTART
        elif symbol == key.ENTER:
            if self.current_index == 0:
                self.director.game_init()  # start the game
                self.director.state = 'GAME'
                for item in self.menu_items:  # clean menu text
                    item.delete()
            elif self.current_index == 1:
                pass
            elif self.current_index == 2:
                pyglet.app.exit()


class GameWindow(pyglet.window.Window):
    """
    Game Director managing all actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # location of upper left corner
        self.set_location(50, 50)
        # frame rate is set to 1 as the game not need more updates
        self.frame_rate = 1
        # main batch for all objects
        self.batch = pyglet.graphics.Batch()

        # start game with menu
        self.state = 'MENU'
        self.menu = Menu(self)
        self.menu.menu_init()

    def game_init(self):
        # allow to choose set feature
        # for quickstart game (for beginners) make one feature False - 27 cards in game
        # for normal game leave all as True - 81 cards in game
        FeatSwitch = namedtuple("FeatSwitch", "pattern number shape color_name")

        # random select features for the game after user menu choice
        features = 4 * [True]
        if self.menu.set_feature == FEATURES_QUICKSTART:
            features[random.randint(0, 3)] = False
        feat_switch = FeatSwitch(*features)

        self.cards = Cards(rows=3, cols=4, feat_switch=feat_switch, batch=self.batch)

        self.score = TextCountable(self.width-180, self.height-20, "Sets found: ", batch=self.batch)
        self.score.count = 0

        self.cards_number_display = TextCountable(self.width - 450, self.height - 20, "Cards left: ", batch=self.batch)
        self.cards_number_display.count = self.cards.number_of_cards_left()

    def game(self):
        if len(self.cards.card_clicked) == 3:
            if self.cards.check_if_cards_are_set(self.cards.card_clicked):
                print(">>>> Found a set!")
                self.score.count += 1
                for c in self.cards.card_clicked:
                    # Add three new cards and remove old ones
                    old_x, old_y = c.x, c.y
                    # remove card from both total cards list and used (drawn on screen)
                    self.cards.cards_used.remove(c)
                    self.cards.cards.remove(c)
                    # remove card sprite from batch
                    c.delete()
                    # if there are cards left in total cards list, draw one of them
                    # take note that this loop will execute always three times (three cards drawn)
                    if self.cards.number_of_cards_left() > 0:
                        self.cards.draw_single_random(old_x, old_y)
            else:
                # if cards are not a set, unselect them
                for c in self.cards.card_clicked:
                    c.scale = SCALE_CARD_UNSELECTED

            self.cards.card_clicked = []
            # display number of cards left on top of window
            self.cards_number_display.count = self.cards.number_of_cards_left()

            # this is end of game when thare are no left sets visible
            if not self.cards.check_if_set_exists_in_cards_used():
                self.state = 'END'

    def end(self):
        if self.cards.cards_used:
            for c in self.cards.cards_used:
                c.delete()  # remove any leftover cards
        txt = TextBase(self.width // 2, self.height // 2, "End of the Game", batch=self.batch)
        txt.font_size += 10
        print("END GAME")

    def on_mouse_press(self, x, y, button, modifiers):
        # When player clicks mouse left button and clicked point (x,y) is inside card box
        if button == mouse.LEFT and self.state == 'GAME':
            for card in self.cards.cards_used:
                if card.is_in_the_box(x, y):
                    # that card is scaled up and added into clicked list if it was not there before
                    if card not in self.cards.card_clicked:
                        card.scale = SCALE_CARD_SELECTED
                        self.cards.card_clicked.append(card)
                        print(card)
                    else:
                        card.scale = SCALE_CARD_UNSELECTED
                        self.cards.card_clicked.remove(card)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if self.state == "MENU":
            self.menu.choose_menu_item(symbol)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        if self.state == 'GAME':
            self.game()
        elif self.state == 'END':
            self.end()


if __name__ == '__main__':
    window = GameWindow(width=1024, height=600, caption="Sets", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
