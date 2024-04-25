import pyglet

from game.configuration import BackgroundColor
from game.director import GameDirector

pyglet.resource.path = ["res", "res/images", "res/sounds", "res/fonts"]
pyglet.resource.reindex()


if __name__ == "__main__":
    window = GameDirector(width=1024, height=600, caption="Set Game", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.gl.glClearColor(*BackgroundColor.rgb01)
    pyglet.app.run()
