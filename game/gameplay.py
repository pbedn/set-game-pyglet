import random

from pyglet.shapes import Box

from pyglet.window import key

from .configuration import config
from . import (DEBUG, FEATURES_QUICKSTART,
               RIGHT_HUD_TEXT, LEFT_HUD_TEXT, END_GAME_TEXT, HINT_SETS_COUNT_TEXT,
               FeatSwitch)
from .cards import Cards
from .fsm import State
from .hud import TextCountable, TextBase


class GamePlay(State):
    def execute(self):
        if self.d.keys[key.R]:
            self.d.fsm.transition('toGAME')
        if self.d.keys[key.F10]:
            self.d.fsm.transition('toMENU')
        if self.d.keys[key.N] and not self.d.new_column_used:
            self.add_new_column()
            self.d.new_column_used = True

        two_cards = self.d.cards.get_two_cards_from_random_set()

        # display number of sets visible on board
        if self.d.keys[key.G] and two_cards:
            self.remove_text_hint()  # if exists
            self.display_text_hint()

        # display two cards from correct set on board
        if self.d.keys[key.H] and two_cards:
            self.remove_text_hint()  # if exists
            for c in self.d.cards.card_clicked:
                c.outline_delete()
            self.d.cards.card_clicked = []
            self.display_hint()

        clicked = self.d.cards.card_clicked
        # If player clicked three cards check if they are a set
        if len(clicked) == 3:
            if self.d.cards.check_if_cards_are_set(clicked):
                print(">>>> Found a set!") if DEBUG else None
                self.d.score.count += 3

                # reset deck to 12 cards if 15 were in the game
                add_new_cards = False if len(self.d.cards.cards_used) == 15 else True

                for c in clicked:
                    c.outline_delete()
                    self.remove_old_card_and_add_new_one(c, add_new_cards)
            else:
                # un-select them, and decrease score
                self.d.score.count = self.d.score.count - 1 if self.d.score.count > 0 else 0
                for c in self.d.cards.card_clicked:
                    c.outline_delete()

            self.d.cards.card_clicked = []

            # display number of cards left on top of window
            self.d.cards_number_display.count = self.d.cards.number_of_cards_left()

            self.remove_text_hint()  # if exists

        # end of game when there are no left sets
        if not self.d.cards.check_if_set_exists_in_cards_used():
            self.d.fsm.transition('toEND')

    def display_hint(self):
        """Select and scale up two cards"""
        self.d.cards.card_hint1.outline_draw(self.d.batch)
        self.d.cards.card_hint1.clicked = True
        self.d.cards.card_clicked.append(self.d.cards.card_hint1)
        self.d.cards.card_hint2.outline_draw(self.d.batch)
        self.d.cards.card_hint2.clicked = True
        self.d.cards.card_clicked.append(self.d.cards.card_hint2)

    def display_text_hint(self):
        """Display number of sets left when hint is requested"""
        txt = HINT_SETS_COUNT_TEXT.format(self.d.cards.number_of_sets_left)
        self.d.cards_number_display_hint = TextBase(self.d.width // 2 + 100, self.d.height - 75, txt,
                                                    batch=self.d.batch)
        self.d.cards_number_display_hint.anchor_x = 'right'
        self.d.cards_number_display_hint.font_size -= 5

    def remove_text_hint(self):
        """Remove silently hint text if exists"""
        try:
            self.d.cards_number_display_hint.delete()
        except AttributeError:
            pass

    def remove_old_card_and_add_new_one(self, c, add_new_cards):
        """
        First remove card from cards list and its sprite
        next add new in the same place
        """
        old_x, old_y = c.x, c.y
        self.d.cards.cards_used.remove(c)
        self.d.cards.cards.remove(c)
        c.delete()  # remove card sprite from batch

        if self.d.cards.number_of_cards_left() > 0 and add_new_cards:
            self.d.cards.draw_single_random(old_x, old_y)

    def add_new_column(self):
        """Draw additional fifth column of three cards at player request"""
        subtract_from_x = 100
        self.d.cards.redraw_columns(subtract_from_x)
        self.d.cards.draw_random(800 + config.corner_margin.x - subtract_from_x)

        # update cards display
        self.d.cards_number_display.count = self.d.cards.number_of_cards_left()

    def on_mouse_press(self, x, y, button, modifiers):
        for card in self.d.cards.cards_used:
            # when clicked point (x,y) is inside card box
            if self.d.is_in_the_box(card, x, y):
                # that card is scaled up and added into clicked list if it was not there before
                if card not in self.d.cards.card_clicked:
                    card.outline_draw(self.d.batch, self.d.foreground)
                    self.d.cards.card_clicked.append(card)
                    print(card) if DEBUG else None
                else:
                    self.d.cards.card_clicked.remove(card)
                    card.outline_delete()
        if self.d.is_in_the_box(self.d.menu_box, x, y):
            self.d.fsm.transition('toMENU')

    def on_mouse_motion(self, x, y):
        cursor = self.d.get_system_mouse_cursor(self.d.CURSOR_DEFAULT)
        self.d.set_mouse_cursor(cursor)
        for card in self.d.cards.cards_used:
            if self.d.is_in_the_box(card, x, y):
                cursor = self.d.get_system_mouse_cursor(self.d.CURSOR_HAND)
                self.d.set_mouse_cursor(cursor)


class GameEnd(State):
    def execute(self):
        if self.d.keys[key.R]:
            self.d.fsm.transition('toGAME')
        if self.d.keys[key.F10]:
            self.d.fsm.transition('toMENU')


class TransitionToGame(State):
    def __init__(self, to_state, *args):
        super().__init__(*args)
        self.to_state = to_state

    def execute(self):
        self.d.delete_all_objects()
        self.d.new_column_used = False

        # randomly select features for the game after user menu choice
        # quickstart game (one feature is False) - 27 cards in game
        # normal game - 81 cards in game
        features = 4 * [True]
        if self.d.set_feature == FEATURES_QUICKSTART:
            features[random.randint(0, 3)] = False
        feat_switch = FeatSwitch(*features)

        # initialize deck of cards with selected features
        self.d.cards = Cards(self.d, rows=3, cols=4, feat_switch=feat_switch)

        # initialize upper hud text
        self.d.score = TextCountable(self.d.width - 180,
                                     self.d.height - 20,
                                     RIGHT_HUD_TEXT,
                                     batch=self.d.batch)
        self.d.score.font_size -= 10
        self.d.score.count = 0
        self.d.cards_number_display = TextCountable(self.d.width - 450,
                                                    self.d.height - 20,
                                                    LEFT_HUD_TEXT,
                                                    batch=self.d.batch)
        self.d.cards_number_display.font_size -= 10
        self.d.cards_number_display.count = self.d.cards.number_of_cards_left()
        self.d.logo = TextBase(
            260, self.d.height - 20,
            "Mode: {}".format(self.d.set_feature), font_size=20, align='left',
            batch=self.d.batch)
        self.d.logo.font_size -= 10

        self.d.menu_btn = TextBase(
            60, self.d.height - 20,
            "Menu".format(self.d.set_feature),
            batch=self.d.batch, group=self.d.foreground)
        self.d.menu_btn.font_size -= 10
        self.d.menu_box = Box(
            0, self.d.height - 45, 120, 45,
            thickness=1,
            color=config.outline_box.color,
            batch=self.d.batch, group=self.d.foreground
        )

        self.d.fsm.set_state('GAME')


class TransitionToEnd(State):
    def __init__(self, to_state, *args):
        super().__init__(*args)
        self.to_state = to_state

    def execute(self):
        # remove any leftover cards from screen
        if len(self.d.cards.cards_used) > 0:
            for c in self.d.cards.cards_used:
                c.delete()
            self.d.cards.cards_used = []

        self.d.text_end_game = TextBase(self.d.width // 2, self.d.height // 2, END_GAME_TEXT, batch=self.d.batch)
        self.d.text_end_game.font_size += 10

        self.d.fsm.set_state('END')
