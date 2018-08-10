from collections import namedtuple

DEBUG = True
COLORS = ['red', 'purple', 'green']
SHAPES = ['oval', 'diamond', 'squiggle']
NUMBERS = ['one', 'two', 'three']
PATTERNS = ['solid', 'striped', 'outlined']
FEATURES = {'color_name': COLORS, 'shape': SHAPES, 'number': NUMBERS, 'pattern': PATTERNS}
SCALE_CARD_SELECTED = 0.80
SCALE_CARD_UNSELECTED = 0.70
MENU_START_GAME_TEXT = "Start Game"
MENU_END_GAME_TEXT = "Exit"
MENU_TEXT_FEATURES_QUICKSTART = "Quickstart: 3 features"
MENU_TEXT_FEATURES_NORMAL = "Normal: 4 features"
FEATURES_QUICKSTART = 'quickstart'
FEATURES_NORMAL = 'normal'
END_GAME_TEXT = "End of the Game"
RIGHT_HUD_TEXT = "Score: "
LEFT_HUD_TEXT = "Cards left: "

# coordinates [x, y, right: x + width, top: y + height] of card image on viewport
Box = namedtuple("Box", "x y right top")

FeatSwitch = namedtuple("FeatSwitch", "pattern number shape color_name")
