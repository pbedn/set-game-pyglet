import pyglet
from pyglet.window import key, mouse

from .gameplay import GamePlay, GameEnd, TransitionToGame, TransitionToEnd
from .menu import GameMenu, TransitionToMenu
from . import Constants, DEBUG
from .fsm import FSM
from .resources import read_images_from_disk, create_card_sprites


class GameDirector(pyglet.window.Window):
    """
    Game Director managing all actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(50, 50)  # location of upper left window corner
        self.frame_rate = 0.1
        self.batch = pyglet.graphics.Batch()

        cursor = self.get_system_mouse_cursor(self.CURSOR_HAND)
        self.set_mouse_cursor(cursor)

        self.first_run = [True] * 2
        self.new_column_used = False

        card_scale = 0.8
        self.constants = Constants(card_scale=card_scale)

        seq = read_images_from_disk()
        self.preloaded = create_card_sprites(seq, self.constants.scale_card_unselected)

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
        try:
            self.cards_number_display_hint.delete()
        except AttributeError:
            pass
        self.logo.delete()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        This method should be inside GamePlay
        but mouse functionality cannot be moved in a way like keys handler
        """
        if button == mouse.LEFT and self.fsm.cur_state == self.fsm.states['GAME']:
            self.fsm.states['GAME'].on_mouse_press(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        """Global key shortcuts"""
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        self.fsm.execute()
