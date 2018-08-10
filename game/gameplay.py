import random
from pyglet.window import key

from . import (DEBUG, SCALE_CARD_SELECTED, SCALE_CARD_UNSELECTED, FEATURES_QUICKSTART,
               RIGHT_HUD_TEXT, LEFT_HUD_TEXT, END_GAME_TEXT, FeatSwitch)
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

        # display a two cards hint
        if self.d.keys[key.H] and self.d.cards.get_two_cards_from_random_set():
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
                    self.remove_old_card_and_add_new_one(c, add_new_cards)
            else:
                # un-select them, and decrease score
                self.d.score.count = self.d.score.count - 1 if self.d.score.count > 0 else 0
                for c in self.d.cards.card_clicked:
                    c.scale = SCALE_CARD_UNSELECTED

            self.d.cards.card_clicked = []

            # display number of cards left on top of window
            self.d.cards_number_display.count = self.d.cards.number_of_cards_left()

        # end of game when there are no left sets
        if not self.d.cards.check_if_set_exists_in_cards_used():
            self.d.fsm.transition('toEND')

    def display_hint(self):
        """Select and scale up two cards"""
        self.d.cards.card_hint1.scale = SCALE_CARD_SELECTED
        self.d.cards.card_hint1.clicked = True
        self.d.cards.card_clicked.append(self.d.cards.card_hint1)
        self.d.cards.card_hint2.scale = SCALE_CARD_SELECTED
        self.d.cards.card_clicked.append(self.d.cards.card_hint2)

    def remove_old_card_and_add_new_one(self, c, add_new_cards):
        """
        First remove card from cards list and its sprite
        next add new one in the same place
        """
        old_x, old_y = c.x, c.y
        self.d.cards.cards_used.remove(c)
        self.d.cards.cards.remove(c)
        c.delete()  # remove card sprite from batch

        if self.d.cards.number_of_cards_left() > 0 and add_new_cards:
            self.d.cards.draw_single_random(old_x, old_y)

    def add_new_column(self):
        """Draw additional fifth column of three cards at player request"""
        self.d.cards.draw_random(800)

        # update cards display
        self.d.cards_number_display.count = self.d.cards.number_of_cards_left()


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
        print(__class__.__name__) if DEBUG else None

        self.d.delete_all_objects()

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
        self.d.score.count = 0
        self.d.cards_number_display = TextCountable(self.d.width - 450,
                                                    self.d.height - 20,
                                                    LEFT_HUD_TEXT,
                                                    batch=self.d.batch)
        self.d.cards_number_display.count = self.d.cards.number_of_cards_left()

        self.d.fsm.set_state('GAME')


class TransitionToEnd(State):
    def __init__(self, to_state, *args):
        super().__init__(*args)
        self.to_state = to_state

    def execute(self):
        print(__class__.__name__) if DEBUG else None

        # remove any leftover cards from screen
        if len(self.d.cards.cards_used) > 0:
            for c in self.d.cards.cards_used:
                c.delete()
            self.d.cards.cards_used = []

        self.d.text_end_game = TextBase(self.d.width // 2, self.d.height // 2, END_GAME_TEXT, batch=self.d.batch)
        self.d.text_end_game.font_size += 10

        self.d.fsm.set_state('END')
