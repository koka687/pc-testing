class Figure:
    FIGURES = ["трикутник", "квадрат", "коло"]

    def __init__(self, figure_type, length):
        if figure_type not in self.FIGURES:
            raise AssertionError("Недопустима фігура")
        if length <= 0:
            raise AssertionError("Довжина має бути більше 0")
        self.type = figure_type
        self.length = length

    @property
    def get_figure_length(self):
        return self.length