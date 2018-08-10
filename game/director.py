import pyglet
from pyglet.window import key, mouse

from .gameplay import GamePlay, GameEnd, TransitionToGame, TransitionToEnd, TransitonToRedraw
from .menu import GameMenu, TransitionToMenu
from . import (DEBUG, SCALE_CARD_UNSELECTED, SCALE_CARD_SELECTED)
from .fsm import FSM


class GameDirector(pyglet.window.Window):
    """
    Game Director managing all actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(50, 50)  # location of upper left window corner
        self.frame_rate = 0.1
        self.batch = pyglet.graphics.Batch()

        self.first_run = [True] * 2

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        # Set GAME Finite State Machine states and transitions
        self.fsm = FSM()
        self.fsm.states['MENU'] = GameMenu(self)
        self.fsm.states['GAME'] = GamePlay(self)
        self.fsm.states['END'] = GameEnd(self)
        self.fsm.transitions['toMENU'] = TransitionToMenu('MENU', self)
        self.fsm.transitions['toGAME'] = TransitionToGame('GAME', self)
        self.fsm.transitions['toEND'] = TransitionToEnd('END', self)
        self.fsm.transitions['toREDRAW'] = TransitonToRedraw('GAME', self)

        self.fsm.transition('toMENU')

    def delete_all_objects(self):
        """Remove all visible sprite cards and text labels from screen"""
        if self.first_run:
            self.first_run.pop()
            return
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

    def on_mouse_press(self, x, y, button, modifiers):
        """
        This method should be inside GamePlay
        but mouse functionality cannot be moved in a way like keys handler
        """
        if button == mouse.LEFT and self.fsm.cur_state == self.fsm.states['GAME']:
            for card in self.cards.cards_used:
                # when clicked point (x,y) is inside card box
                if card.is_in_the_box(x, y):
                    # that card is scaled up and added into clicked list if it was not there before
                    if card not in self.cards.card_clicked:
                        card.scale = SCALE_CARD_SELECTED
                        self.cards.card_clicked.append(card)
                        print(card, card.row, card.col, 'CLICK') if DEBUG else None
                        print(self.cards.grid[card.row][card.col], 'GRID')
                    else:
                        card.scale = SCALE_CARD_UNSELECTED
                        self.cards.card_clicked.remove(card)

    def on_key_press(self, symbol, modifiers):
        """Global key shortcuts"""
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        self.fsm.execute()
