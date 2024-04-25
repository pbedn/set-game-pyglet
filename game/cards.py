from __future__ import annotations

import itertools
import random
from itertools import combinations

import pyglet
from pyglet.shapes import Box

from .configuration import config
from .constants import COLORS, FEATURES, NUMBERS, PATTERNS, SHAPES


class Card(pyglet.sprite.Sprite):
    """Single Card sprite object"""

    def __init__(self, img, card_color, card_shape, card_pattern, card_number):
        super().__init__(img)
        self.color_name = card_color
        self.shape = card_shape
        self.pattern = card_pattern
        self.number = card_number
        self._outline = None

    def outline_draw(self, batch, group):
        self._outline = Box(
            self.x,
            self.y,
            self.width + config.outline_box.size,
            self.height + config.outline_box.size,
            thickness=config.outline_box.thickness,
            color=config.outline_box.color,
            batch=batch,
            group=group,
        )
        self._outline.draw()

    def outline_delete(self):
        try:
            self._outline.delete()
        except AttributeError:
            pass

    def __str__(self):
        return f"Card: {self.color_name}, {self.shape}, {self.pattern}, {self.number}, {(self.x, self.y, self.width, self.height)}"


class Cards:
    """Manager of all cards that are displayed on the screen
    and generated but hidden for the user
    """

    def __init__(self, director, rows, cols, feat_switch):
        self.rows = rows
        self.cols = cols
        self.d = director

        self.preloaded = create_card_sprites(
            self.d.seq, self.d.constants.scale_card_unselected
        )
        self.cards = select_features(self.preloaded, feat_switch)
        self._check_cards_number(feat_switch)

        self.cards_used = []
        self.card_clicked = []

        for i in range(self.cols):
            self.draw_random(i * 200 + config.corner_margin.x)

    def _check_cards_number(self, feat_switch):
        """Assert that number of cards after feature removal is correct
        All four features should have 81 cards
        Quickstart game (one feature off) - 27 cards
        """
        total = 81
        for attribute in FEATURES.keys():
            if not getattr(feat_switch, attribute):
                total /= 3
        assert (
            len(self.cards) == total
        ), "Number of cards after features removal is wrong"

    def __iter__(self):
        for card in self.cards:
            yield card

    def draw_selected(self, card, x, y):
        """Set attributes and add to batch a selected card"""
        card.update(x, y)
        card.batch = self.d.batch

    def draw_random(self, x_offset):
        """Draw one column of random cards

        :param x_offset: x position offset of first drawn card
        """
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        for i, card in enumerate(cards):
            if i >= self.rows:
                break
            self.draw_selected(card, x_offset, 150 * i + config.corner_margin.y)
            self.cards_used.append(card)

    def redraw_columns(self, x_sub):
        """Draw one column of random cards"""
        for card in self.cards_used:
            card.outline_delete()
            card.update(card.x - x_sub, card.y)

    def draw_single_random(self, x, y):
        """Draw single random card at given coordinates"""
        cards = [c for c in self.cards if c not in self.cards_used]
        random.shuffle(cards)
        card = cards[0]
        self.draw_selected(card, x, y)
        self.cards_used.append(card)

    @staticmethod
    def check_if_cards_are_set(cards_list):
        """Detailed conditions for correct set are described in README.
        If set consists of one or three elements then it is correct
        according to game rules, therefore it has to be different than 2
        """
        assert len(cards_list) == 3, "Cards clicked length should be 3"
        result = True
        for attribute in FEATURES.keys():
            set_a = {
                getattr(cards_list[0], attribute),
                getattr(cards_list[1], attribute),
                getattr(cards_list[2], attribute),
            }
            result = result and len(set_a) != 2
        return result

    def check_if_set_exists_in_cards_used(self):
        """Iterate through all cards drawn on screen
        make combinations of three cards from them
        And check if they are a set
        """
        result = []
        for c in combinations(self.cards_used, 3):
            result.append(self.check_if_cards_are_set(c))
        return True if True in result else False

    def get_two_cards_from_random_set(self):
        list_of_sets = [
            c
            for c in combinations(self.cards_used, 3)
            if self.check_if_cards_are_set(c)
        ]
        self.number_of_sets_left = len(list_of_sets)
        if self.number_of_sets_left > 0:
            random.shuffle(list_of_sets)
            self.card_hint1 = list_of_sets[0][0]
            self.card_hint2 = list_of_sets[0][1]
            return True
        return False

    def number_of_cards_left(self):
        """Number of cards that are not draw on the screen"""
        num = len(self.cards) - len(self.cards_used)
        return num if num >= 0 else 0


def select_features(cards, switch):
    """Remove selected feature from total cards list

    :param cards: list if cards image sprites
    :param switch: namedtuple with boolean features
    :return: List of cards after removal selected feature
    """
    new_cards = [i for i in cards]

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


def create_card_sprites(seq, scale):
    """Iterate through image sequence and create card sprites

    :return: List containing all cards read from image resources
    """
    card_list = []
    card_seq = iter(seq)
    for pattern, shape, color, number in itertools.product(
        PATTERNS, SHAPES, COLORS, NUMBERS
    ):
        card_sprite = Card(
            img=card_seq.__next__(),
            card_color=color,
            card_shape=shape,
            card_number=number,
            card_pattern=pattern,
        )
        card_sprite.scale = scale
        card_list.append(card_sprite)
    return card_list
