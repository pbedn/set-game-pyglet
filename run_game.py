import pyglet

pyglet.resource.path = ['res']
pyglet.resource.reindex()

from game.director import GameDirector

if __name__ == '__main__':
    window = GameDirector(width=1024, height=600, caption="Sets", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
