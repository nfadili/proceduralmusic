import unittest

class TestSong(unittest.TestCase):

    def test_parseTempoData_valid(self):
        integerTempo = 120      #hex(120) = 07 A1 20
        self.assertEqual(parseTempoData(integerTempo), [int(7, 16), int(A1, 16), int(20, 16)])

    def test_parseTempoData_invalid(self):
        integerTempo = -100
        self.assertRaises(TempoError, parseTempoData, integerTempo)

    def test_addNoteToTrack_valid(self):
        pass

    def test_addRestToTrack_valid(self):
        pass

    def test_markSongEnd(self):
        pass

if __name__ == '__main__':
    unittest.main()
