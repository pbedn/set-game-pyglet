import random
from collections import namedtuple

import pyglet
from pyglet.window import mouse, key

from . import (FEATURES_QUICKSTART, DEBUG, SCALE_CARD_UNSELECTED,
               SCALE_CARD_SELECTED, END_GAME_TEXT, LEFT_HUD_TEXT, RIGHT_HUD_TEXT)
from .cards import Cards
from .hud import TextBase, TextCountable
from .menu import Menu
from .resources import read_images_from_disk, create_card_sprites


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

        # one time use variable to control loading of images
        self.preload = True

        # start game with menu
        self.state = 'MENU'
        self.menu = Menu(self)
        self.menu.menu_init()

        self.loading = TextBase(150, 500, "Loading ...", batch=self.batch)

    def game_init(self):
        # Test if all cards are correctly preloaded
        assert len(self._cards) == 81, "Cards Preload Test"

        # allow to choose set feature
        # for quickstart game (for beginners) make one feature False - 27 cards in game
        # for normal game leave all as True - 81 cards in game
        FeatSwitch = namedtuple("FeatSwitch", "pattern number shape color_name")

        # random select features for the game after user menu choice
        features = 4 * [True]
        if self.menu.set_feature == FEATURES_QUICKSTART:
            features[random.randint(0, 3)] = False
        feat_switch = FeatSwitch(*features)

        self.cards = Cards(self._cards, rows=3, cols=4, feat_switch=feat_switch, batch=self.batch)

        self.score = TextCountable(self.width - 180, self.height - 20, RIGHT_HUD_TEXT, batch=self.batch)
        self.score.count = 0

        self.cards_number_display = TextCountable(self.width - 450, self.height - 20, LEFT_HUD_TEXT, batch=self.batch)
        self.cards_number_display.count = self.cards.number_of_cards_left()

    def game(self):
        if len(self.cards.card_clicked) == 3:
            if self.cards.check_if_cards_are_set(self.cards.card_clicked):
                if DEBUG: print(">>>> Found a set!")
                self.score.count += 3
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
                # if cards are not a set, unselect them, and decrease score
                self.score.count = self.score.count - 1 if self.score.count > 0 else 0
                for c in self.cards.card_clicked:
                    c.scale = SCALE_CARD_UNSELECTED

            self.cards.card_clicked = []
            # display number of cards left on top of window
            self.cards_number_display.count = self.cards.number_of_cards_left()

            # this is end of game when thare are no left sets visible
            if not self.cards.check_if_set_exists_in_cards_used():
                self.state = 'END'

    def end(self):
        if len(self.cards.cards_used) > 0:
            for c in self.cards.cards_used:
                c.delete()  # remove any leftover cards from screen
            self.cards.cards_used = []
        self.text_end_game = TextBase(self.width // 2, self.height // 2, END_GAME_TEXT, batch=self.batch)
        self.text_end_game.font_size += 10

    def _delete_all_objects(self):
        """Remove all visible sprite cards and text labels from screen"""
        if len(self.cards.cards_used) > 0:
            for c in self.cards.cards_used:
                c.delete()
            self.cards.cards_used = []
        self.score.delete()
        self.cards_number_display.delete()
        try:
            self.text_end_game.delete()
        except AttributeError:
            pass

    def game_restart(self):
        self._delete_all_objects()
        self.game_init()
        self.state = 'GAME'

    def menu_restart(self):
        self._delete_all_objects()
        self.menu.menu_init()
        self.state = 'MENU'

    def on_mouse_press(self, x, y, button, modifiers):
        # When player clicks mouse left button and clicked point (x,y) is inside card box
        if button == mouse.LEFT and self.state == 'GAME':
            for card in self.cards.cards_used:
                if card.is_in_the_box(x, y):
                    # that card is scaled up and added into clicked list if it was not there before
                    if card not in self.cards.card_clicked:
                        card.scale = SCALE_CARD_SELECTED
                        self.cards.card_clicked.append(card)
                        if DEBUG: print(card)
                    else:
                        card.scale = SCALE_CARD_UNSELECTED
                        self.cards.card_clicked.remove(card)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if symbol == key.R and self.state != 'MENU':
            self.game_restart()
        if symbol == key.F10 and self.state != 'MENU':
            self.menu_restart()
        if self.state == 'MENU':
            self.menu.choose_menu_item(symbol)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        if self.state == 'MENU' and self.preload:
            # card images loading during menu display
            seq = read_images_from_disk()
            self._cards = create_card_sprites(seq)  # TODO: Why is it so long?
            self.loading.delete()
            self.preload = False
        if self.state == 'GAME':
            self.game()
        elif self.state == 'END':
            self.end()
