import pyglet
from pyglet.window import key, mouse

from .gameplay import GamePlay, GameEnd, TransitionToGame, TransitionToEnd
from .menu import GameMenu, TransitionToMenu
from . import Constants
from .fsm import FSM
from .resources import read_images_from_disk


class GameDirector(pyglet.window.Window):
    """
    Game Director managing all actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(50, 50)  # location of upper left window corner
        self.frame_rate = 0.1
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Group(order=0)
        self.foreground = pyglet.graphics.Group(order=1)

        cursor = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
        self.set_mouse_cursor(cursor)

        self.first_run = [True] * 2
        self.new_column_used = False

        card_scale = 0.8
        self.constants = Constants(card_scale=card_scale)

        self.seq = read_images_from_disk()

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
                c.outline_delete()
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
        # todo: global objects aggregator then loop over it would be better
        # group ?
        self.menu_box.delete()
        self.menu_btn.delete()

    @staticmethod
    def is_in_the_box(box, x, y):
        if box.x <= x <= box.x + box.width and box.y <= y <= box.y + box.height:
            return True

    def on_mouse_press(self, x, y, button, modifiers):
        """Global mouse press"""
        if button == mouse.LEFT and self.fsm.cur_state == self.fsm.states['GAME']:
            self.fsm.states['GAME'].on_mouse_press(x, y, button, modifiers)
        elif button == mouse.LEFT and self.fsm.cur_state == self.fsm.states['MENU']:
            self.fsm.states['MENU'].on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Global mouse motion"""
        if self.fsm.cur_state == self.fsm.states['GAME']:
            self.fsm.states['GAME'].on_mouse_motion(x, y)
        elif self.fsm.cur_state == self.fsm.states['MENU']:
            self.fsm.states['MENU'].on_mouse_motion(x, y)

    def on_key_press(self, symbol, modifiers):
        """Global key shortcuts"""
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        self.fsm.execute()
