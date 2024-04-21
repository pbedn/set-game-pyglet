import pyglet

pyglet.resource.path = ['res', 'res/images', 'res/sounds', 'res/fonts']
pyglet.resource.reindex()

from game.director import GameDirector


if __name__ == '__main__':
    window = GameDirector(width=1024, height=600, caption="Set Game", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.gl.glClearColor(0.173, 0.243, 0.314, 1.0)
    pyglet.app.run()
