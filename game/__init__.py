from collections import namedtuple

DEBUG = False
COLORS = ['red', 'purple', 'green']
SHAPES = ['oval', 'diamond', 'squiggle']
NUMBERS = ['one', 'two', 'three']
PATTERNS = ['solid', 'striped', 'outlined']
FEATURES = {'color_name': COLORS, 'shape': SHAPES, 'number': NUMBERS, 'pattern': PATTERNS}
# coordinates [x, y, right: x + width, top: y + height] of card image on viewport
Box = namedtuple("Box", "x y right top")
SCALE_CARD_SELECTED = 0.80
SCALE_CARD_UNSELECTED = 0.70
MENU_TEXT_FEATURES_QUICKSTART = "Quickstart: 3 features"
MENU_TEXT_FEATURES_NORMAL = "Normal: 4 features"
FEATURES_QUICKSTART = 'quickstart'
FEATURES_NORMAL = 'normal'
