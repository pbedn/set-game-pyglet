import pyglet
from pyglet.window import key

from . import (MENU_TEXT_FEATURES_QUICKSTART, FEATURES_QUICKSTART, FEATURES_NORMAL,
               MENU_TEXT_FEATURES_NORMAL, MENU_START_GAME_TEXT, MENU_END_GAME_TEXT)
from .hud import TextBase


class Menu:
    def __init__(self, director):
        self.director = director

    def menu_init(self):
        start_game_menu_item = TextBase(self.director.width // 2, self.director.height // 2 + 100, MENU_START_GAME_TEXT, batch=self.director.batch)
        start_game_menu_item.bold = True
        start_game_menu_item.font_size += 10
        features_menu_item = TextBase(self.director.width // 2, self.director.height // 2, MENU_TEXT_FEATURES_QUICKSTART, batch=self.director.batch)
        end_game_menu_item = TextBase(self.director.width // 2, self.director.height // 2 - 100, MENU_END_GAME_TEXT, batch=self.director.batch)
        self.menu_items = [start_game_menu_item, features_menu_item, end_game_menu_item]
        self.current_index = 0
        self.current_selection = self.menu_items[0]
        self.set_feature = FEATURES_QUICKSTART  # used to save number of features user (3 or 4) for cards init

        help = """
        Menu: Quickstart or Normal
        R - Restart during gameplay with previous settings
        F10 - Go to menu
        ESCAPE - Exit app
        """
        help_menu_item = TextBase(self.director.width // 2,
                                  self.director.height // 8,
                                  help,
                                  batch=self.director.batch,
                                  multiline=True,
                                  width=self.director.width)
        help_menu_item.font_size -= 18
        self.menu_items.append(help_menu_item)

    def choose_menu_item(self, symbol):
        if symbol == key.DOWN:
            self.current_selection.bold = False
            self.current_selection.font_size -= 10
            self.current_index += 1
            if self.current_index > 2:
                self.current_index = 0
            self.current_selection = self.menu_items[self.current_index]
            self.current_selection.bold = True
            self.current_selection.font_size += 10
        elif symbol == key.UP:
            self.current_selection.bold = False
            self.current_selection.font_size -= 10
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = 2
            self.current_selection = self.menu_items[self.current_index]
            self.current_selection.bold = True
            self.current_selection.font_size += 10
        elif self.current_index == 1 and symbol == key.RIGHT:
            self.set_feature = FEATURES_NORMAL
            self.current_selection.text = MENU_TEXT_FEATURES_NORMAL
        elif self.current_index == 1 and symbol == key.LEFT:
            self.set_feature = FEATURES_QUICKSTART
            self.current_selection.text = MENU_TEXT_FEATURES_QUICKSTART
        elif symbol == key.ENTER:
            if self.current_index == 0:
                self.director.game_init()  # start the game
                self.director.state = 'GAME'
                for item in self.menu_items:  # clean menu text
                    item.delete()
            elif self.current_index == 1:
                pass
            elif self.current_index == 2:
                pyglet.app.exit()
