import Song
from constants import *

# This class enforces music theory rules while generating sequences of notes for
# insertion into a Song object. Sequences are inserted into individual tracks within
# the Song object.
class NoteSequence:

    def __init__(self, key, voice, sequenceLength,):
        self.length = sequenceLength
        self.voice = voice
        self.key = key
        self.sequence = []

    def __str__(self):
        case = {
            1 : 'BASS',
            2 : 'TENOR',
            3 : 'ALTO',
            4 : 'SOPRANO'
        }
        return 'Key: ' + self.key + '\n' + case.get(self.voice) + '\n' + str(self.sequence)


if __name__ == '__main__':
    seq = NoteSequence('C', SOPRANO, 20)
    print(str(seq))
