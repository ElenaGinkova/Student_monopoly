import unittest
from GuitarHW import Tone 
from GuitarHW import Interval 
from GuitarHW import Chord

class TestTone(unittest.TestCase):
 
    def test_tone_initialization_and_str(self):
        c_sharp = Tone("C#")
        self.assertEqual(str(c_sharp), "C#")
 
class TestInterval(unittest.TestCase):
 
    def test_interval_initialization_and_str(self):
        minor_third = Interval(3)
        self.assertEqual(str(minor_third), "minor 3rd")
 
    def test_interval_wrap_around(self):
        interval = Interval(13) 
        self.assertEqual(str(interval), "minor 2nd")
 
class TestChord(unittest.TestCase):
 
    def test_chord_initialization_and_str(self):
        c, d_sharp, g = Tone("C"), Tone("D#"), Tone("G")
        chord = Chord(c, d_sharp, g)
        self.assertEqual(str(chord), "C-D#-G")
 
    def test_chord_unique_tones(self):
        c, another_c = Tone("C"), Tone("C")
        with self.assertRaises(TypeError) as context:
            Chord(c, another_c)
        self.assertEqual(str(context.exception), "Cannot have a chord made of only 1 unique tone")
 
    def test_is_minor(self):
        c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
        self.assertTrue(c_minor_chord.is_minor())
 
        c_not_minor_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
        self.assertFalse(c_not_minor_chord.is_minor())
 
    def test_is_major(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        self.assertTrue(c_major_chord.is_major())
 
        c_not_major_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
        self.assertFalse(c_not_major_chord.is_major())
 
    def test_is_power_chord(self):
        c_power_chord = Chord(Tone("C"), Tone("F"), Tone("G"))
        self.assertTrue(c_power_chord.is_power_chord())
 
        c_not_power_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        self.assertFalse(c_not_power_chord.is_power_chord())
 
    def test_add_tones_creates_chord(self):
        c, g = Tone("C"), Tone("G")
        result_chord = c + g
        self.assertEqual(str(result_chord), "C-G")
 
    def test_subtract_tones_creates_interval(self):
        c, g = Tone("C"), Tone("G")
        result_interval = g - c
        self.assertEqual(str(result_interval), "perfect 5th")
 
    def test_add_tone_and_interval(self):
        c = Tone("C")
        result_tone = c + Interval(7)
        self.assertEqual(str(result_tone), "G")
 
    def test_subtract_interval_from_tone(self):
        c = Tone("C")
        perfect_fifth = Interval(7)
        result_tone = c - perfect_fifth
        self.assertEqual(str(result_tone), "F")
 
    def test_invalid_operations(self):
        c = Tone("C")
        perfect_fifth = Interval(7)
        with self.assertRaises(TypeError) as context:
            perfect_fifth + c
        self.assertEqual(str(context.exception), "Invalid operation")
 
    def test_add_intervals(self):
        perfect_fifth = Interval(7)
        minor_third = Interval(3)
        result_interval = perfect_fifth + minor_third
        self.assertEqual(str(result_interval), "minor 7th")
 
    def test_chord_add_tone(self):
        c5_chord = Chord(Tone("C"), Tone("G"))
        result_chord = c5_chord + Tone("E")
        self.assertEqual(str(result_chord), "C-E-G")
 
    def test_chord_subtract_tone(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        result_chord = c_major_chord - Tone("E")
        self.assertEqual(str(result_chord), "C-G")
 
    def test_chord_subtract_nonexistent_tone(self):
        c_power_chord = Chord(Tone("C"), Tone("G"))
        with self.assertRaises(TypeError) as context:
            result_chord = c_power_chord - Tone("E")
        self.assertEqual(str(context.exception), "Cannot remove tone E from chord C-G")
 
    def test_chord_add_chord(self):
        c5_chord = Chord(Tone("C"), Tone("G"))
        another_chord = Chord(Tone("A"), Tone("B"))
        result_chord = c5_chord + another_chord
        self.assertEqual(str(result_chord), "C-G-A-B")
 
    def test_transposed_chord(self):
        c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
        d_minor_chord = c_minor_chord.transposed(Interval(2))
        self.assertEqual(str(d_minor_chord), "D-F-A")
 
        a_sharp_minor_chord = d_minor_chord.transposed(-Interval(4))
        self.assertEqual(str(a_sharp_minor_chord), "A#-C#-F")
 
class TestAdditionalCases(unittest.TestCase):
 
    def test_large_intervals(self):
        c = Tone("C")
        self.assertEqual(str(c + Interval(24)), "C")  
        self.assertEqual(str(c + Interval(25)), "C#") 
 
    def test_negative_interval_transpose(self):
        f_sixth_ninth_chord = Chord(Tone("F"), Tone("C"), Tone("D"), Tone("A"), Tone("G"))
        result_chord = f_sixth_ninth_chord.transposed(-Interval(2))
        self.assertEqual(str(result_chord), "D#-F-G-A#-C")
 
    def test_invalid_right_addition(self):
        c = Tone("C")
        perfect_fifth = Interval(7)
        with self.assertRaises(TypeError) as context:
            perfect_fifth + c 
        self.assertEqual(str(context.exception), "Invalid operation")
 
    def test_chord_subtract_to_single_tone_exception(self):
        c_power_chord = Chord(Tone("C"), Tone("G"))
        with self.assertRaises(TypeError) as context:
            result_chord = c_power_chord - Tone("G")  
        self.assertEqual(str(context.exception), "Cannot have a chord made of only 1 unique tone")
 
    def test_chord_add_with_duplicate_tones(self):
        c5_chord = Chord(Tone("C"), Tone("G"))
        duplicate_tone_chord = Chord(Tone("G"), Tone("A"))
        result_chord = c5_chord + duplicate_tone_chord
        self.assertEqual(str(result_chord), "C-G-A") 
        
    def test_transpose_with_large_intervals(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        transposed_chord = c_major_chord.transposed(Interval(24))
        self.assertEqual(str(transposed_chord), "C-E-G")
        
 
if __name__ == "__main__":
    unittest.main()
 