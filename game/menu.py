from functools import wraps

import pyglet
from pyglet.window import key
from pyglet.shapes import Box

from .configuration import config
from .fsm import State
from .constants import *
from .hud import TextBase


def _formatter(func):
    """Change font attributes of previous and current menu item selection"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.d.current_selection.bold = False
        self.d.current_selection.font_size -= 3
        func(self, *args, **kwargs)
        self.d.current_selection = self.d.menu_items[self.d.current_index]
        self.d.current_selection.bold = True
        self.d.current_selection.font_size += 3

    return wrapper


class GameMenu(State):
    def __init__(self, *args):
        super().__init__(*args)
        self.start_box = None
        self.option_box = None
        self.exit_box = None

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
        self.start_box.delete()
        self.option_box.delete()
        self.exit_box.delete()
        self.d.fsm.transition('toGAME')

    def menu_boxes(self, batch):
        self.start_box = Box(
            285, 400, 460, 85,
            thickness=1,
            color=config.outline_box.color,
            batch=batch
        )
        # self.start_box.visible = False
        self.start_box.draw()
        self.option_box = Box(
            285, 300, 460, 85,
            thickness=1,
            color=config.outline_box.color,
            batch=batch
        )
        # self.option_box.visible = False
        self.option_box.draw()
        self.exit_box = Box(
            285, 200, 460, 85,
            thickness=1,
            color=config.outline_box.color,
            batch=batch
        )
        # self.exit_box.visible = False
        self.exit_box.draw()

    def execute(self):
        self.menu_boxes(self.d.batch)
        if self.d.keys[key.DOWN] and self.d.current_index < 2:
            self.selection_down()
        elif self.d.keys[key.UP] and self.d.current_index > 0:
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

    def on_mouse_press(self, x, y, button, modifiers):
        if self.d.is_in_the_box(self.start_box, x, y):
            self.start_game()
        elif self.d.is_in_the_box(self.option_box, x, y):
            if self.d.current_selection.text == MENU_TEXT_FEATURES_QUICKSTART:
                self.d.set_feature = FEATURES_NORMAL
                self.d.current_selection.text = MENU_TEXT_FEATURES_NORMAL
            else:
                self.d.set_feature = FEATURES_QUICKSTART
                self.d.current_selection.text = MENU_TEXT_FEATURES_QUICKSTART
        elif self.d.is_in_the_box(self.exit_box, x, y):
            pyglet.app.exit()

    @_formatter
    def select_index(self, i):
        self.d.current_index = i

    def on_mouse_motion(self, x, y):
        if self.d.is_in_the_box(self.start_box, x, y):
            self.select_index(0)
        elif self.d.is_in_the_box(self.option_box, x, y):
            self.select_index(1)
        elif self.d.is_in_the_box(self.exit_box, x, y):
            self.select_index(2)


class TransitionToMenu(State):
    def __init__(self, to_state, *args):
        super().__init__(*args)
        self.to_state = to_state

    def execute(self):
        self.d.delete_all_objects()

        start_game_menu_item = TextBase(self.d.width // 2,
                                        self.d.height // 2 + 150,
                                        MENU_START_GAME_TEXT,
                                        batch=self.d.batch)
        start_game_menu_item.bold = True
        start_game_menu_item.font_size += 10
        features_menu_item = TextBase(self.d.width // 2,
                                      self.d.height // 2 + 50,
                                      MENU_TEXT_FEATURES_QUICKSTART,
                                      batch=self.d.batch)
        end_game_menu_item = TextBase(self.d.width // 2,
                                      self.d.height // 2 - 50,
                                      MENU_END_GAME_TEXT,
                                      batch=self.d.batch)
        self.d.menu_items = [start_game_menu_item, features_menu_item, end_game_menu_item]
        self.d.current_index = 0
        self.d.current_selection = self.d.menu_items[0]

        self.d.set_feature = FEATURES_QUICKSTART

        help_menu_item = TextBase(self.d.width // 2,
                                  self.d.height // 6,
                                  HELP_TEXT,
                                  batch=self.d.batch,
                                  multiline=True,
                                  width=self.d.width)
        help_menu_item.font_size -= 18
        self.d.menu_items.append(help_menu_item)

        help_menu_item2 = TextBase(self.d.width // 2 + 400,
                                   self.d.height // 6,
                                   HELP_TEXT_2,
                                   batch=self.d.batch,
                                   multiline=True,
                                   width=self.d.width)
        help_menu_item2.font_size -= 18
        self.d.menu_items.append(help_menu_item2)
