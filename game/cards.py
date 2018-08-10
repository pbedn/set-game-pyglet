import random
from itertools import combinations

import pyglet

from . import SCALE_CARD_UNSELECTED, SCALE_CARD_SELECTED, Box, FEATURES
from .resources import select_features, create_card_sprites, read_images_from_disk


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
        self.row = 0
        self.col = 0

        # Coordinates of box at init are out of real window
        self.box = Box(5000, 5000, 100, 100)

    def set_position_and_box(self, x, y):
        """Set position of sprite in window and create box variable"""
        self.position = (x, y)
        self.box = Box(x, y, x+self.width, y+self.height)

    def is_in_the_box(self, x, y):
        """Check if point (x,y) is inside card box (rectangle)"""
        if self.box.x <= x <= self.box.right \
                and self.box.y <= y <= self.box.top:
            return True

    def __str__(self):
        return "Card: {}, {}, {}, {}".format(self.color_name, self.shape, self.pattern, self.number)


class Cards:
    """
    Manager of all cards that are displayed on the screen
    and generated but hidden for the user
    """
    def __init__(self, director, rows, cols, feat_switch):
        self.rows = rows
        self.cols = cols
        self.grid = [[None] * (self.cols + 1) for _ in range(self.rows)]
        self.director = director

        # preload images from disk
        # TODO: this is slow process (CPU)
        seq = read_images_from_disk()
        preloaded = create_card_sprites(seq)
        self.cards = select_features(preloaded, feat_switch)
        self._check_cards_number(feat_switch)

        self.cards_used = []
        self.card_clicked = []

        for i in range(self.cols):
            self.draw_random(i, 200)

    def _check_cards_number(self, feat_switch):
        """
        Assert that number of cards after feature removal is correct
        All four features should have 81 cards
        Quickstart game (one feature off) - 27 cards
        """
        total = 81
        for attribute in FEATURES.keys():
            if not getattr(feat_switch, attribute):
                total /= 3
        assert len(self.cards) == total, "Number of cards after features removal is wrong"

    def __iter__(self):
        for card in self.cards:
            yield card

    def set_grid(self, row, col, card):
        """Assign card to the grid"""
        self.grid[row][col] = card
        card.row = row
        card.col = col

    def draw_selected(self, card, x, y):
        """Set attributes and add to batch a selected card"""
        card.set_position_and_box(x, y)
        card.batch = self.director.batch # FIXME: Do I need director here?

    def draw_random(self, col, offset):
        """
        Draw one column of random cards

        :param col: column
        """
        x = col * offset
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        for i, card in enumerate(cards):
            if i >= self.rows:
                break
            self.draw_selected(card, x + 25, 150 * i + 100)
            self.cards_used.append(card)
            self.set_grid(row=i, col=col, card=card)

    def draw_single_random(self, x, y):
        """Draw single random card at given coordinates"""
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        card = cards[0]
        self.draw_selected(card, x, y)
        self.cards_used.append(card)

    @staticmethod
    def check_if_cards_are_set(cards_list):
        """
        Detailed conditions for correct set are described in README.
        If set consists of one or three elements then it is correct
        according to game rules, therefore it has to be different than 2
        """
        assert len(cards_list) == 3, "Cards clicked length should be 3"
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
        """
        result = []
        for c in combinations(self.cards_used, 3):
            result.append(self.check_if_cards_are_set(c))
        return True if True in result else False

    def get_two_cards_from_random_set(self):
        list_of_sets = [c for c in combinations(self.cards_used, 3) if self.check_if_cards_are_set(c)]
        number_of_sets_left = len(list_of_sets)
        if number_of_sets_left > 0:
            random.shuffle(list_of_sets)
            self.card_hint1 = list_of_sets[0][0]
            self.card_hint2 = list_of_sets[0][1]
            return True
        return False

    def number_of_cards_left(self):
        """Number of cards that are not draw on the screen"""
        num = len(self.cards) - len(self.cards_used)
        return num if num >= 0 else 0

    def display_hint(self):
        """Select and scale up two cards"""
        self.card_hint1.scale = SCALE_CARD_SELECTED
        self.card_hint1.clicked = True
        self.card_clicked.append(self.card_hint1)
        self.card_hint2.scale = SCALE_CARD_SELECTED
        self.card_clicked.append(self.card_hint2)

    def remove_old_card_and_add_new_one(self, c, add_new_cards):
        """
        First remove card from cards list and its sprite
        next add new one in the same place
        """
        old_x, old_y = c.x, c.y
        self.cards_used.remove(c)
        self.cards.remove(c)
        c.delete()  # remove card sprite from batch
        # self.grid[c.row][c.col] = False

        if self.number_of_cards_left() > 0 and add_new_cards:
            self.draw_single_random(old_x, old_y)

    def add_new_column(self):
        """Draw additional fifth column of three cards at player request"""
        self.draw_random(col=1, offset=800)

        # update cards display
        self.director.cards_number_display.count = self.number_of_cards_left()

    def redraw_cards(self):
        """Redraw 12 cards to be in 4 columns only"""
        # for card in self.director.cards.card_clicked:
        #     print("Redraw, row, col", card.row, card.col)
        #     if card.col == 3:
        #         card_to_be_moved = card
        #     else:
        #         card_empty = card
        #
        # x, y = card_empty.x, card_empty.y
        # # card_to_be_moved.set_position_and_box(card_empty.x, card_empty.y)
        # # card_to_be_moved.row, card_to_be_moved.col = card_empty.row, card_empty.col
        # card_empty.__dict__.update(card_to_be_moved.__dict__)
        # card_to_be_moved.set_position_and_box(x, y)
        pass

