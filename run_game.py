"""
Run the game with --old-graphic parameter to use different cards images
'sets-green.png, sets-purple.png, sets-red.png'
otherwise 'new-sets.png' are used
"""

import sys

import pyglet

pyglet.resource.path = ['res']
pyglet.resource.reindex()

from game.director import GameDirector

try:
    user_input = sys.argv[1]
except IndexError:
    user_input = False

USE_NEW_GRAPHIC_SET = False if user_input == '--old-graphic' else True

if __name__ == '__main__':
    window = GameDirector(USE_NEW_GRAPHIC_SET,
                          width=1024, height=600, caption="Sets", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
