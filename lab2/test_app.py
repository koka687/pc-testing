import pytest
from app import Figure

# Фікстура рівня module (використовується в двох тестах)
@pytest.fixture(scope="module")
def allowed_figures():
    return Figure.FIGURES

# Фікстура для перевірки довжини 10
@pytest.fixture
def figure_len_10():
    return Figure("квадрат", 10)

# 1. Параметризований тест для всіх дозволених фігур
@pytest.mark.parametrize("figure", Figure.FIGURES)
def test_allowed_figure(figure):
    assert Figure(figure, 1).type == figure

# 2. Тест з фікстурою (довжина 10) + маркер unit
@pytest.mark.unit
def test_figure_len_10(figure_len_10):
    assert figure_len_10.get_figure_length == 10
    assert figure_len_10.type == "квадрат"

# 3. Тест для неправильного типу фігури
def test_invalid_figure_type():
    with pytest.raises(AssertionError):
        Figure("ромб", 5)

# 4. Параметризований тест для неправильних значень довжини
@pytest.mark.parametrize("invalid_length", [0, -5])
def test_invalid_length(invalid_length):
    with pytest.raises(AssertionError):
        Figure("квадрат", invalid_length)

# 5. Використання фікстури зі scope="module" (Тест 1) + маркер unit
@pytest.mark.unit
def test_module_fixture_one(allowed_figures):
    assert "коло" in allowed_figures

# 6. Використання фікстури зі scope="module" (Тест 2)
def test_module_fixture_two(allowed_figures):
    assert len(allowed_figures) == 3

# 7. Навмисно зламаний тест для команди -x
def test_broken_intentionally():
    assert Figure("квадрат", 5).get_figure_length == 999