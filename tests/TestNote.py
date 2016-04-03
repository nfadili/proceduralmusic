import sys
sys.path.append('../src')

import unittest

class TestNoteMethods(unittest.TestCase):

    def test_parsePitch_valid_NoAccidentals(self):
        self.assertEqual(parsePitch('C_0'), 0)
        self.assertEqual(parsePitch('C_1'), 12)
        self.assertEqual(parsePitch('C_8'), 96)
        self.assertEqual(parsePitch('F_3'), 41)
        self.assertEqual(parsePitch('B_0'), 11)

    def test_parsePitch_invalid_NoAccidentals(self):
        self.assertRaises(PitchError, parsePitch, 'C_9')
        self.assertRaises(PitchError, parsePitch, 'G_-1')

    def test_parsePitch_valid_WithAccidentals(self):
        self.assertEqual(parsePitch('C#_5'), 61)
        self.assertEqual(parsePitch('D#_3'), 38)
        self.assertEqual(parsePitch('E#_3'), 41)
        self.assertEqual(parsePitch('B#_0'), 12)

    def test_parsePitch_invalid_WithAccidentals(self):
        self.assertRaises(PitchError, parsePitch, 'E#_10')
        self.assertRaises(PitchError, parsePitch, 'A#_-1')

    def test_parsePitch_Rest(self):
        self.assertEqual(parsePitch('R'), -1)

if __name__ == '__main__':
    unittest.main()
