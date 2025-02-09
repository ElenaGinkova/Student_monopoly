import unittest
import importlib
from unittest.mock import patch, call
 
import study
 
 
class TestFifthHomework(unittest.TestCase):
 
    def setUp(self) -> None:
        class BulgarianKid(metaclass=study.Kid):
            def __call__(self, present):
                pass
 
            def be_bad_kid(self):
                raise ValueError("I am going to 33")
 
        class ChineseKid(metaclass=study.Kid):
            def __call__(self, present):
                pass
 
        class NigerianKid(metaclass=study.Kid):
            def __call__(self, present):
                pass
 
            def kill_people(self):
                raise ValueError("There is no fun like 33")
 
        self.bulgarian_kid_class = BulgarianKid
        self.chinese_kid_class = ChineseKid
        self.nigerian_kid_class = NigerianKid
        self.santa = study.Santa()
 
        def get_letter_1(kid):
            return f""" Здрасти Дядо Коледа,
                Бях относително добро дете
                Моля купи ми "   LADA NIVA"
                Поздрави,
                          {id(kid)}
            """
 
        def get_letter_1_not_signed():
            return f""" Здрасти Дядо Коледа,
                            Бях относително добро дете
                            Моля купи ми "   LADA NIVA 2025 "
                            Поздрави,
                        """
 
        def get_letter_2_(kid):
            return f""" Здрасти Дядо Коледа,
                                        Нямам добри оценки, но поне имам добро сърце
                                        Моля купи ми "dvokolka s turbo"
                                        Поздрави,
                                        {id(kid)}
                                    """
 
        def get_letter_2_not_signed():
            return f""" Здрасти Дядо Коледа,
                                        Нямам добри оценки, но поне имам добро сърце
                                        Моля купи ми "dvokolka s turbo"
                                        Поздрави,
                                    """
 
        self.get_letter_1 = get_letter_1
        self.get_letter_1_not_signed = get_letter_1_not_signed
        self.get_letter_2 = get_letter_2_
        self.get_letter_2_not_signed = get_letter_2_not_signed
 
    def tearDown(self) -> None:
        importlib.reload(study)
 
    def test_kid_metaclass_instances_throw_not_implemented_if___call___not_defined_in_derived_class(self):
        with self.assertRaises(NotImplementedError):
            class InvalidKidClass(metaclass=study.Kid):
                pass
 
    def test_santa_is_singleton(self):
        s1 = study.Santa()
        s2 = study.Santa()
        self.assertIs(s1, s2)
 
    def test_a_kid_is_bad_kid_in_xmas_with_other_good_kid(self):
        chinese_kid = self.chinese_kid_class()
        self.santa @ self.get_letter_1(chinese_kid)
        nigerian_kid = self.nigerian_kid_class()
        try:
            nigerian_kid.kill_people()
        except ValueError:
            pass
        with patch.object(self.nigerian_kid_class, "__call__") as mock:
            self.santa.xmas()
            mock.assert_called_with("coal")
 
    def test_most_wanted_present_is_derived_from_good_kids(self):
        nigerian_kid = self.nigerian_kid_class()
        bulgarian_kid = self.bulgarian_kid_class()
        try:
            nigerian_kid.kill_people()
        except ValueError:
            pass
 
        try:
            bulgarian_kid.be_bad_kid()
        except ValueError:
            pass
        chinese_kid = self.chinese_kid_class()
        self.santa @ self.get_letter_1(chinese_kid)
        with patch.object(self.nigerian_kid_class, "__call__") as nig_mock, \
                patch.object(self.chinese_kid_class, "__call__") as chin_mock, \
                patch.object(self.bulgarian_kid_class, "__call__") as bulg_mock:
            self.santa.xmas()
            nig_mock.assert_called_once_with("coal")
            bulg_mock.assert_called_once_with("coal")
            chin_mock.assert_called_once_with("   LADA NIVA")
 
    def test_only_bad_children_no_one_gets_present(self):
        nigerian_kid = self.nigerian_kid_class()
        bulgarian_kid = self.bulgarian_kid_class()
        try:
            nigerian_kid.kill_people()
        except ValueError:
            pass
 
        try:
            bulgarian_kid.be_bad_kid()
        except ValueError:
            pass
 
        with patch.object(self.nigerian_kid_class, "__call__") as nig_mock, \
                patch.object(self.nigerian_kid_class, "__call__") as bulg_mock:
            self.santa.xmas()
            nig_mock.assert_not_called()
            bulg_mock.assert_not_called()
 
    def test_good_kids_get_most_wanted_present_and_bad_kids_dont(self):
        nigerian_kid = self.nigerian_kid_class()
        bulgarian_kid = self.bulgarian_kid_class()
        try:
            nigerian_kid.kill_people()
        except ValueError:
            pass
 
        try:
            bulgarian_kid.be_bad_kid()
        except ValueError:
            pass
 
        bulgarian_kid_2 = self.bulgarian_kid_class()
        chinese_kid_1 = self.chinese_kid_class()
        chinese_kid_2 = self.chinese_kid_class()
        nigerian_kid_2 = self.nigerian_kid_class()
        nigerian_kid_3 = self.nigerian_kid_class()
        chinese_kid_3 = self.chinese_kid_class()
 
        self.santa @ self.get_letter_1(bulgarian_kid_2)
        self.santa @ self.get_letter_1(chinese_kid_1)
        self.santa @ self.get_letter_2(chinese_kid_2)
 
        with patch.object(self.nigerian_kid_class, "__call__") as nig_mock, \
                patch.object(self.chinese_kid_class, "__call__") as chin_mock, \
                patch.object(self.bulgarian_kid_class, "__call__") as bulg_mock:
            self.santa.xmas()
            self.assertEqual(nig_mock.call_count, 3)
            self.assertEqual(chin_mock.call_count, 3)
            self.assertEqual(bulg_mock.call_count, 2)
            self.assert_mock_called_with_arguments_n_times(chin_mock, 2, "   LADA NIVA")
            self.assert_mock_called_with_arguments_n_times(chin_mock, 1, "dvokolka s turbo")
            self.assert_mock_called_with_arguments_n_times(nig_mock, 1, "coal")
            self.assert_mock_called_with_arguments_n_times(nig_mock, 2, "   LADA NIVA")
            self.assert_mock_called_with_arguments_n_times(bulg_mock, 1, "   LADA NIVA")
            self.assert_mock_called_with_arguments_n_times(bulg_mock, 1, "coal")
 
    def assert_mock_called_with_arguments_n_times(self, mock, times, *args):
        current = call(*args)
        filtered_args = [c for c in mock.call_args_list if c == current]
        self.assertEqual(len(filtered_args), times)
 
    def test_bad_kid_does_bad_things_and_then_tries_to_get_present_and_fails(self):
        nigerian_kid = self.nigerian_kid_class()
        try:
            nigerian_kid.kill_people()
        except ValueError:
            pass
 
        self.santa @ self.get_letter_1(nigerian_kid)
        with patch.object(self.nigerian_kid_class, "__call__") as mock:
            self.santa.xmas()
            mock.assert_called_once_with("coal")
 
    def test_iterate_santa_more_than_ones(self):
        bulgarian_kid = self.bulgarian_kid_class()
        self.santa @ self.get_letter_2(bulgarian_kid)
        for index in range(2):
            for present in self.santa:
                self.assertEqual(present, "dvokolka s turbo")
 
    @unittest.skip("Не съм сигурен дали можем да преизползваме една iterator instance")
    def test_iterator_reset(self):
        bulgarian_kid = self.bulgarian_kid_class()
        self.santa @ self.get_letter_2(bulgarian_kid)
 
        iterator = iter(self.santa)
        for index in range(2):
            for present in iterator:
                self.assertEqual(present, "dvokolka s turbo")
 
    def test_kid_overrides_its_present_and_order_doesnt_change(self):
        bulgarian_kid = self.bulgarian_kid_class()
        chinese_kid = self.chinese_kid_class()
        self.santa(bulgarian_kid, '"skuter"')
        self.santa(chinese_kid, "'kniga'")
        self.santa(bulgarian_kid, "'vodka'")
 
        results = ["vodka", "kniga"]
        for index, element in enumerate(self.santa):
            self.assertEqual(results[index], element)
 
    def test_empty_iterator_after_xmas(self):
        nigerian_kid = self.nigerian_kid_class()
        bulgarian_kid = self.bulgarian_kid_class()
 
        self.santa(nigerian_kid, self.get_letter_1_not_signed())
        self.santa(bulgarian_kid, self.get_letter_2_not_signed())
 
        results = ["   LADA NIVA 2025 ", "dvokolka s turbo"]
        for index, present in enumerate(self.santa):
            self.assertEqual(results[index], present)
        self.santa.xmas()
        iterator = iter(self.santa)
        with self.assertRaises(StopIteration):
            next(iterator)
 
    def test_empty_iterator_on_load(self):
        iterator = iter(self.santa)
        with self.assertRaises(StopIteration):
            next(iterator)
 
    def test_bad_child_wants_present_and_other_children_with_no_wanted_presents_take_it(self):
        nigerian_kid = self.nigerian_kid_class()
        chinese_kid = self.chinese_kid_class()
        bulgarian_kid = self.bulgarian_kid_class()
        try:
            nigerian_kid.kill_people()
        except ValueError:
            pass
        self.santa(nigerian_kid, self.get_letter_2_not_signed())
        with patch.object(self.nigerian_kid_class, "__call__") as nig_mock, \
                patch.object(self.bulgarian_kid_class, "__call__") as bulg_mock, \
                patch.object(self.chinese_kid_class, "__call__") as chin_mock:
            self.santa.xmas()
            nig_mock.assert_called_once_with("coal")
            bulg_mock.assert_called_once_with("dvokolka s turbo")
            chin_mock.assert_called_once_with("dvokolka s turbo")
 
    def test_bad_kid_reset_for_next_xmas(self):
        nigerian_kid = self.nigerian_kid_class()
        try:
            nigerian_kid.kill_people()
        except ValueError:
            pass
        self.santa(nigerian_kid, self.get_letter_2_not_signed())
        with patch.object(self.nigerian_kid_class, "__call__") as mock:
            self.santa.xmas()
            mock.assert_called_once_with("coal")
 
        self.santa(nigerian_kid, self.get_letter_2_not_signed())
        with patch.object(self.nigerian_kid_class, "__call__") as mock:
            self.santa.xmas()
            mock.assert_called_once_with("dvokolka s turbo")
 
    def test_kids_grow_up_even_no_wants_sends_present_and_xmas_is_trigged(self):
        nigerian_kid = self.nigerian_kid_class()
        for i in range(5):
            self.santa.xmas()
        chinese_kid = self.chinese_kid_class()
        self.santa(chinese_kid, self.get_letter_2_not_signed())
 
        with patch.object(self.chinese_kid_class, "__call__") as chin_mock, \
                patch.object(self.nigerian_kid_class, "__call__") as nig_mock:
            self.santa.xmas()
            chin_mock.assert_called_once_with("dvokolka s turbo")
            nig_mock.assert_not_called()
 
if __name__ == '__main__':
    unittest.main()