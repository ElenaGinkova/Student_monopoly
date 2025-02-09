import unittest
from secret import validate_recipe, RuinedNikuldenDinnerError
from unittest.mock import patch, mock_open

class TestNikuldenValidator(unittest.TestCase):
    def test_valid_recipe(self):
        valid_file = "доста доста риба лала Рибена глава съм аз" # fake file content
        with patch("builtins.open", mock_open(read_data = valid_file)): # immitates open built in func and gives my fake file content
            self.assertTrue(validate_recipe("someFile.txt"))

    def test_invalid_recipe(self):
        invalid_file = "рецепта с рЙба няма нищо гладни сме малко соона"
        with patch("builtins.open", mock_open(read_data = invalid_file)):
            self.assertFalse(validate_recipe("somefile.txt"))

    def test_bad_recipe_file(self):
        errors = [OSError, IOError]
        for error in errors:
            with patch("builtins.open", side_effect = error):
                with self.assertRaises(RuinedNikuldenDinnerError):
                    validate_recipe("file.txt")

if __name__ == '__main__':
    unittest.main()