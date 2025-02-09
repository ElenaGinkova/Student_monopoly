import unittest
from GuitarHW import Tone 
from GuitarHW import Interval 
from GuitarHW import Chord
class TestMusicTheory(unittest.TestCase):

    def test_tone_initialization(self):
        c_sharp = Tone("C#")
        self.assertEqual(str(c_sharp), "C#")

    def test_interval_initialization(self):
        minor_third = Interval(3)
        self.assertEqual(str(minor_third), "minor 3rd")

    def test_chord_initialization(self):
        c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
        self.assertEqual(str(c_minor_chord), "C-D#-G")

    def test_chord_unique_tones(self):
        c = Tone("C")
        another_c = Tone("C")
        with self.assertRaises(TypeError) as context:
            Chord(c, another_c)
        self.assertEqual(str(context.exception), "Cannot have a chord made of only 1 unique tone")

    def test_csus4_chord(self):
        c = Tone("C")
        another_c = Tone("C")
        f = Tone("F")
        csus4_chord = Chord(c, f, another_c)
        self.assertEqual(str(csus4_chord), "C-F")

    def test_f_sixth_ninth_chord(self):
        f_sixth_ninth_chord = Chord(Tone("F"), Tone("C"), Tone("D"), Tone("A"), Tone("G"))
        self.assertEqual(str(f_sixth_ninth_chord), "F-G-A-C-D")

    def test_c_minor_chord_is_minor(self):
        c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
        self.assertTrue(c_minor_chord.is_minor())

    def test_c_not_minor_chord(self):
        c_not_minor_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
        self.assertFalse(c_not_minor_chord.is_minor())

    def test_c_major_chord_is_major(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        self.assertTrue(c_major_chord.is_major())

    def test_c_not_major_chord(self):
        c_not_major_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
        self.assertFalse(c_not_major_chord.is_major())

    def test_c_power_chord(self):
        c_power_chord = Chord(Tone("C"), Tone("F"), Tone("G"))
        self.assertTrue(c_power_chord.is_power_chord())

    def test_c_not_power_chord(self):
        c_not_power_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        self.assertFalse(c_not_power_chord.is_power_chord())

    def test_add_tones(self):
        c = Tone("C")
        g = Tone("G")
        result_chord = c + g
        self.assertEqual(str(result_chord), "C-G")

    def test_subtract_tones(self):
        c = Tone("C")
        g = Tone("G")
        result_interval = g - c
        self.assertEqual(str(result_interval), "perfect 5th")

    def test_add_interval_to_tone(self):
        c = Tone("C")
        perfect_fifth = Interval(7)
        result_tone = c + perfect_fifth
        self.assertEqual(str(result_tone), "G")

    def test_add_full_octave_to_tone(self):
        c = Tone("C")
        result_tone = c + Interval(12)
        self.assertEqual(str(result_tone), "C")

    def test_add_interval_to_tone_g(self):
        g = Tone("G")
        perfect_fifth = Interval(7)
        result_tone = g + perfect_fifth
        self.assertEqual(str(result_tone), "D")

    def test_subtract_interval_from_tone(self):
        c = Tone("C")
        perfect_fifth = Interval(7)
        result_tone = c - perfect_fifth
        self.assertEqual(str(result_tone), "F")

    def test_add_intervals(self):
        perfect_fifth = Interval(7)
        minor_third = Interval(3)
        result_interval = perfect_fifth + minor_third
        self.assertEqual(str(result_interval), "minor 7th")

    def test_add_chord_and_tone(self):
        c5_chord = Chord(Tone("C"), Tone("G"))
        result_chord = c5_chord + Tone("E")
        self.assertEqual(str(result_chord), "C-E-G")

    def test_subtract_from_major_chord(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        result_chord = c_major_chord - Tone("E")
        self.assertEqual(str(result_chord), "C-G")

    def test_c_power_chord_subtract_g(self):
        c_power_chord = Chord(Tone("C"), Tone("G"))
        with self.assertRaises(TypeError) as context:
            c_power_chord - Tone("G")
        self.assertEqual(str(context.exception), "Cannot have a chord made of only 1 unique tone")

    def test_c_power_chord_subtract_e(self):
        c_power_chord = Chord(Tone("C"), Tone("G"))
        with self.assertRaises(TypeError) as context:
            c_power_chord - Tone("E")
        self.assertEqual(str(context.exception), "Cannot remove tone E from chord C-G")

    def test_add_two_chords(self):
        c5_chord = Chord(Tone("C"), Tone("G"))
        this_other_chord = Chord(Tone("A"), Tone("B"))
        result_chord = c5_chord + this_other_chord
        self.assertEqual(str(result_chord), "C-G-A-B")

    def test_transpose_minor_chord(self):
        c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
        d_minor_chord = c_minor_chord.transposed(Interval(2))
        self.assertEqual(str(d_minor_chord), "D-F-A")

    def test_transpose_a_sharp_minor_chord(self):
        d_minor_chord = Chord(Tone("D"), Tone("F"), Tone("A"))
        a_sharp_minor_chord = d_minor_chord.transposed(-Interval(4))
        self.assertEqual(str(a_sharp_minor_chord), "A#-C#-F")

if __name__ == '__main__':
    unittest.main()