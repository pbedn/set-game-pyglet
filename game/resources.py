import random

import pyglet

from . import FEATURES, PATTERNS, SHAPES, NUMBERS
from . import cards


def read_images_from_disk():
    """
    Read images from disk into sequence and grid

    :return: Dictionary with three image grid sequences
    """
    red_deck = pyglet.image.load('res/sets-red.png')
    green_deck = pyglet.image.load('res/sets-green.png')
    purple_deck = pyglet.image.load('res/sets-purple.png')
    red_deck_seq = pyglet.image.ImageGrid(red_deck, 9, 3, row_padding=2)
    green_deck_seq = pyglet.image.ImageGrid(green_deck, 9, 3, row_padding=2)
    purple_deck_seq = pyglet.image.ImageGrid(purple_deck, 9, 3, row_padding=2)
    seq = {'red': red_deck_seq, 'green': green_deck_seq, 'purple': purple_deck_seq}
    return seq


def select_features(cards, switch):
    """
    Remove selected feature from total cards list

    :param cards: list if cards image sprites
    :param switch: namedtuple with boolean features
    :return: List of cards after removal selected feature
    """
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


def create_card_sprites(seq):
    """
    Iterate through image sequence and create card sprites

    :return: List containing all cards read from image resources
    """
    card_list = []
    for color, s in seq.items():
        card_seq = iter(reversed(s))
        for pattern in PATTERNS:
            for shape in SHAPES:
                for number in NUMBERS:
                    card = card_seq.__next__()
                    card_list.append(cards.Card(card, color, shape, pattern, number))
    return card_list
