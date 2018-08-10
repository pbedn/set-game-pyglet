from functools import wraps

import pyglet
from pyglet.window import key

from .fsm import State
from . import (MENU_TEXT_FEATURES_QUICKSTART, FEATURES_QUICKSTART, FEATURES_NORMAL,
               MENU_TEXT_FEATURES_NORMAL, MENU_START_GAME_TEXT, MENU_END_GAME_TEXT,
               DEBUG)
from .hud import TextBase


def _formatter(func):
    """Change font attributes of previous and current menu item selection"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.d.current_selection.bold = False
        self.d.current_selection.font_size -= 10
        func(self, *args, **kwargs)
        self.d.current_selection = self.d.menu_items[self.d.current_index]
        self.d.current_selection.bold = True
        self.d.current_selection.font_size += 10
    return wrapper


class GameMenu(State):
    def __init__(self, *args):
        super().__init__(*args)

    @_formatter
    def selection_up(self):
        """Re-set menu selection"""
        self.d.current_index -= 1
        if self.d.current_index < 0:
            self.d.current_index = 2

    @_formatter
    def selection_down(self):
        """Re-set menu selection"""
        self.d.current_index += 1
        if self.d.current_index > 2:
            self.d.current_index = 0
        return

    def start_game(self):
        """Remove menu text objects and transition to game"""
        for item in self.d.menu_items:
            item.delete()
        self.d.fsm.transition('toGAME')

    def execute(self):
        if self.d.keys[key.DOWN]:
            self.selection_down()
        elif self.d.keys[key.UP]:
            self.selection_up()

        elif self.d.current_index == 1:
            if self.d.keys[key.RIGHT]:
                self.d.set_feature = FEATURES_NORMAL
                self.d.current_selection.text = MENU_TEXT_FEATURES_NORMAL
            elif self.d.keys[key.LEFT]:
                self.d.set_feature = FEATURES_QUICKSTART
                self.d.current_selection.text = MENU_TEXT_FEATURES_QUICKSTART

        elif self.d.keys[key.ENTER]:
            if self.d.current_index == 0:
                self.start_game()
            elif self.d.current_index == 1:
                pass
            elif self.d.current_index == 2:
                pyglet.app.exit()


class TransitionToMenu(State):
    def __init__(self, to_state, *args):
        super().__init__(*args)
        self.to_state = to_state

    def execute(self):
        print(__class__.__name__) if DEBUG else None
        self.d.delete_all_objects()

        start_game_menu_item = TextBase(self.d.width // 2,
                                        self.d.height // 2 + 100,
                                        MENU_START_GAME_TEXT,
                                        batch=self.d.batch)
        start_game_menu_item.bold = True
        start_game_menu_item.font_size += 10
        features_menu_item = TextBase(self.d.width // 2,
                                      self.d.height // 2,
                                      MENU_TEXT_FEATURES_QUICKSTART,
                                      batch=self.d.batch)
        end_game_menu_item = TextBase(self.d.width // 2,
                                      self.d.height // 2 - 100,
                                      MENU_END_GAME_TEXT,
                                      batch=self.d.batch)
        self.d.menu_items = [start_game_menu_item, features_menu_item, end_game_menu_item]
        self.d.current_index = 0
        self.d.current_selection = self.d.menu_items[0]

        self.d.set_feature = FEATURES_QUICKSTART

        help_txt = """
        Menu Select: Quickstart or Normal
        Key shortcuts:
            R   - Restart
            F10 - Main Menu
            ESC - Exit app
        """
        help_menu_item = TextBase(self.d.width // 2,
                                  self.d.height // 8,
                                  help_txt,
                                  batch=self.d.batch,
                                  multiline=True,
                                  width=self.d.width)
        help_menu_item.font_size -= 18
        self.d.menu_items.append(help_menu_item)
