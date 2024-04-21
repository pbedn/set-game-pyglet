from collections import namedtuple

DEBUG = True
COLORS = ['red', 'purple', 'green']
SHAPES = ['oval', 'diamond', 'squiggle']
NUMBERS = ['one', 'two', 'three']
PATTERNS = ['outlined', 'striped', 'solid']
FEATURES = {'color_name': COLORS, 'shape': SHAPES, 'number': NUMBERS, 'pattern': PATTERNS}
MENU_START_GAME_TEXT = "Start Game"
MENU_END_GAME_TEXT = "Exit"
MENU_TEXT_FEATURES_QUICKSTART = "Quickstart: 3 features"
MENU_TEXT_FEATURES_NORMAL = "Normal: 4 features"
FEATURES_QUICKSTART = 'quickstart'
FEATURES_NORMAL = 'normal'
END_GAME_TEXT = "End of the Game"
RIGHT_HUD_TEXT = "Score: "
LEFT_HUD_TEXT = "Cards left: "
HINT_SETS_COUNT_TEXT = "I see {} sets. And you?"

FeatSwitch = namedtuple("FeatSwitch", "pattern number shape color_name")


class Constants:
    def __init__(self, card_scale):
        self.scale_card_selected = card_scale * 1.2
        self.scale_card_unselected = card_scale


HELP_TEXT = """
        Game difficulty:
        - Quickstart (27 cards in game)
        - Normal     (81 cards in game)
        
        Key shortcuts:
        R   - Restart game
        G   - Display hint (number of sets)
        H   - Display hint (two of three cards from set) 
        N   - Add 5th cards column (currently you can do it only once)
        F10 - Main menu
        ESC - Exit app
        """
