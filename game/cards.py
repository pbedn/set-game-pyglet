import random
from itertools import combinations

import pyglet

from . import SCALE_CARD_UNSELECTED, Box, FEATURES
from .resources import select_features


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


class Cards:
    """
    Manager of all cards that are displayed on the screen

    and generated but hidden for the user
    """
    def __init__(self, cards_preloaded, rows, cols, feat_switch, batch):
        self.rows = rows
        self.cols = cols
        self.batch = batch

        self.cards = select_features(cards_preloaded, feat_switch)
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
