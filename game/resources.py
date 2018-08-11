import random

import pyglet

from . import FEATURES, PATTERNS, SHAPES, NUMBERS, DEBUG
from . import cards


def read_images_from_disk():
    """
    Read images from disk into sequence and grid

    :return: Dictionary with three image grid sequences
    """
    red_deck = pyglet.resource.image('sets-red.png')
    green_deck = pyglet.resource.image('sets-green.png')
    purple_deck = pyglet.resource.image('sets-purple.png')
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

# -----------------------
# Loading Single Image
# -----------------------


colors_single = [('purple',)*27, ('green',)*27, ('red',)*27]
colors_single = [item for sublist in colors_single for item in sublist]
shapes_single = [('diamond',)*3, ('oval',)*3, ('squiggle',)*3]*9
shapes_single = [item for sublist in shapes_single for item in sublist]
numbers_single = ['one', 'two', 'three']*27
patterns_single = [('solid',)*9, ('striped',)*9, ('outlined',)*9]*3
patterns_single = [item for sublist in patterns_single for item in sublist]

complete_list = list(zip(colors_single, shapes_single, numbers_single, patterns_single))


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def read_images_from_disk_single_image(image, rows, columns):
    """
    Read images from disk into sequence and grid

    :return: Image grid sequence
    """
    deck = pyglet.resource.image(image)
    center_image(deck)
    deck_seq = pyglet.image.ImageGrid(deck, rows=rows, columns=columns, row_padding=10, column_padding=10)
    return deck_seq


def create_card_sprites_single_image(seq, scale):
    """
    Iterate through image sequence and create card sprites

    :return: List containing all cards read from image resources
    """
    card_list = []
    cards_iterator = iter(complete_list)

    for image in seq:
        card = cards_iterator.__next__()
        color = card[0]
        shape = card[1]
        number = card[2]
        pattern = card[3]
        card_sprite = cards.Card(image, color, shape, pattern, number)
        card_sprite.scale = scale
        card_list.append(card_sprite)
    return card_list
