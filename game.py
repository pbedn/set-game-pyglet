import pyglet


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(100, 100)
        self.frame_rate = 1/60.0

    def on_draw(self):
        self.clear()

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = GameWindow(width=800, height=600, caption="Sets", resizable=True)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
