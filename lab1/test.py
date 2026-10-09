import unittest
from unittest.mock import patch
from app import validate_number, count_vowels, Figure, get_user_age

class TestApp(unittest.TestCase):
    
    # --- Тестування validate_number ---
    def test_validate_number_correct(self):
        self.assertEqual(5, validate_number(5))
        
    def test_validate_number_value_error(self):
        with self.assertRaises(ValueError):
            validate_number("abc")
            
    def test_validate_number_assert_error(self):
        with self.assertRaises(AssertionError):
            validate_number(-5)

    # --- Тестування count_vowels ---
    def test_count_vowels_empty(self):
        self.assertEqual(0, count_vowels(""))
        
    def test_count_vowels_digits(self):
        self.assertEqual(0, count_vowels("1234567890"))
        
    def test_count_vowels_ukrainian(self):
        self.assertEqual(3, count_vowels("привіт, світ")) # и, і, і

    # --- Тестування Figure ---
    def test_figure_length(self):
        fig = Figure("квадрат", 10)
        self.assertEqual(10, fig.get_figure_length)
        
    def test_figure_angles(self):
        self.assertEqual(4, Figure("квадрат", 5).get_angles())
        self.assertEqual(4, Figure("прямокутник", 5).get_angles())
        self.assertEqual(3, Figure("трикутник", 5).get_angles())
        
    def test_figure_invalid_length(self):
        with self.assertRaises(ValueError):
            Figure("квадрат", 0)
        with self.assertRaises(ValueError):
            Figure("квадрат", -5)
            
    def test_figure_invalid_type(self):
        with self.assertRaises(ValueError):
            Figure("коло", 5)

    # --- Тестування за допомогою subTest ---
    def test_figure_angles_subtest(self):
        figures = {"квадрат": 4, "прямокутник": 4, "трикутник": 3}
        for fig_type, expected_angles in figures.items():
            with self.subTest(fig_type=fig_type):
                fig = Figure(fig_type, 10)
                self.assertEqual(expected_angles, fig.get_angles())

    # --- Тестування за допомогою mock ---
    @patch('builtins.input', return_value='20')
    def test_input_mock(self, mock_input):
        self.assertEqual(20, get_user_age())
        mock_input.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)