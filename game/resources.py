import itertools
import random

import pyglet

from . import FEATURES, PATTERNS, SHAPES, NUMBERS, COLORS
from . import cards


def read_images_from_disk() -> pyglet.image.ImageGrid:
    """
    Read images from disk into sequence, grid and texture

    :return: ImageGrid
    """
    deck = pyglet.resource.image('spritesheet.png')
    deck_seq = pyglet.image.ImageGrid(deck, 9, 9)
    return deck_seq


def select_features(cards, switch):
    """
    Remove selected feature from total cards list

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
    """
    Iterate through image sequence and create card sprites

    :return: List containing all cards read from image resources
    """
    card_list = []
    card_seq = iter(seq)
    for pattern, shape, color, number in itertools.product(PATTERNS, SHAPES, COLORS, NUMBERS):
        card_sprite = cards.Card(
            img=card_seq.__next__(),
            card_color=color,
            card_shape=shape,
            card_number=number,
            card_pattern=pattern
        )
        card_sprite.scale = scale
        card_list.append(card_sprite)
    return card_list
