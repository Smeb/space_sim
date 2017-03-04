class plot_options:
    def __init__(self, title, color):
        self._title = title
        self._color = color

    @property
    def title(self):
        return self._title

    @property
    def color(self):
        return self._color
