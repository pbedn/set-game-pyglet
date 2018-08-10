import random
from pyglet.window import key

from . import (DEBUG, SCALE_CARD_UNSELECTED, FEATURES_QUICKSTART,
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
        if self.d.keys[key.N]:
            self.d.cards.add_new_column()

        # display a two cards hint
        if self.d.keys[key.H] and self.d.cards.get_two_cards_from_random_set():
            self.d.cards.display_hint()

        clicked = self.d.cards.card_clicked
        # If player clicked three cards check if they are a set
        if len(clicked) == 3:
            if self.d.cards.check_if_cards_are_set(clicked):
                print(">>>> Found a set!") if DEBUG else None
                self.d.score.count += 3

                # reset deck to 12 cards if 15 were in the game
                add_new_cards = False if len(self.d.cards.cards_used) == 15 else True

                for c in clicked:
                    self.d.cards.remove_old_card_and_add_new_one(c, add_new_cards)

                # Redraw 12 cards to be in 4 columns and not 5
                if not add_new_cards:
                    if len(self.d.cards.cards_used) > 0:
                        for c in self.d.cards.cards_used:
                            c.delete()
                        self.d.fsm.transition('toREDRAW')
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


class GameEnd(State):
    def execute(self):
        if self.d.keys[key.R]:
            self.d.fsm.transition('toGAME')
        if self.d.keys[key.F10]:
            self.d.fsm.transition('toMENU')


class TransitonToRedraw(State):
    def __init__(self, *args):
        super().__init__(*args)

    def execute(self):
        print(__class__.__name__) if DEBUG else None

        cards_used = list(self.d.cards.cards_used)

        if len(self.d.cards.cards_used) > 0:
            for c in self.d.cards.cards_used:
                c.delete()
            self.d.cards.cards_used = []

        self.d.cards.grid = [[None] * (self.cols + 1) for _ in range(self.rows)]

        # preload images from disk
        # TODO: this is slow process (CPU)
        from .resources import read_images_from_disk, create_card_sprites
        seq = read_images_from_disk()
        preloaded = create_card_sprites(seq)

        new_cards = [i for i in preloaded]

        def remove_cards(pre_card, lst):
            if pre_card not in cards_used:
                lst.remove(pre_card)

        for card in preloaded:
            remove_cards(card, new_cards)

        self.d.cards.cards = new_cards

        self.d.cards.cards_used = []
        self.d.cards.card_clicked = []
        #
        for i in range(self.d.cards.cols):
            self.d.cards.draw_random(i, 200)
        #     x = col * offset
        #     cards = [c for c in self.cards if c not in self.cards_used]
        #     random.shuffle(cards)
        #     for i, card in enumerate(cards):
        #         if i >= self.rows:
        #             break
        #         self.draw_selected(card, x + 25, 150 * i + 100)
        #         self.cards_used.append(card)
        #         self.set_grid(row=i, col=col, card=card)

        self.d.fsm.set_state('GAME')


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
        self.d.feat_switch = FeatSwitch(*features)

        # initialize deck of cards with selected features
        self.d.cards = Cards(self.d, rows=3, cols=4, feat_switch=self.d.feat_switch)

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
