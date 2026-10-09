def validate_number(num):
    if not isinstance(num, (int, float)):
        raise ValueError("Введене значення має бути числом!")
    assert num >= 0, "Число не може бути від'ємним!"
    return num

def count_vowels(text: str) -> int:
    vowels = "аеєиіїоуюяАЕЄИІЇОУЮЯaeiouyAEIOUY"
    return sum(1 for char in text if char in vowels)

class Figure:
    def __init__(self, figure_type, length):
        valid_types = ["квадрат", "прямокутник", "трикутник"]
        if figure_type not in valid_types:
            raise ValueError(f"Невідомий тип фігури: {figure_type}")
        if length <= 0:
            raise ValueError("Довжина має бути більшою за нуль")
        self.figure_type = figure_type
        self.length = length

    @property
    def get_figure_length(self):
        # Помилка була тут: поверталось значення self.length * 2
        # Виправлений варіант:
        return self.length

    def get_angles(self):
        if self.figure_type in ["квадрат", "прямокутник"]:
            return 4
        elif self.figure_type == "трикутник":
            return 3
        return 0

def get_user_age():
    age = input("Введіть ваш вік: ")
    return int(age)