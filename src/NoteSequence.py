import Song
from constants import *

class Note:
    def __init__(self, letter, octave, duration, velocity=20):
         self.letter = letter
         self.octave = octave
         self.duration = duration
         self.velocity = velocity

    def __str__(self):
        return '(' + self.letter + str(self.octave) + ', ' + str(self.duration) + ', ' + str(self.velocity) + ')'

# This class enforces music theory rules while generating sequences of notes for
# insertion into a Song object. Sequences are inserted into individual tracks within
# the Song object.
class NoteSequence:

    def __init__(self, key, voice, sequenceLength):
        self.length = sequenceLength
        self.voice = voice          # Determines starting octave
        self.key = key
        self.noteHistory = []       # Start with only previous note (access with [-1]), then look back farther. (Higher order markov chain).
        self.sequence = self.generate()

    def __str__(self):
        case = {
            2 : 'BASS',
            3 : 'TENOR',
            4 : 'ALTO',
            5 : 'SOPRANO'
        }
        string = 'Key: ' + self.key + '\n' + case.get(self.voice) + '\n['
        for note in self.sequence:
            string += str(note)
        return string + ']'

    def generate(self):
        seq = [Note(self.key, self.voice, EIGHTH, 20)] #Tuple (root, octave, duration, velocity)

        return seq

    def getNextNote(self):
        case = {

        }

    def writeSequenceToTrack(self):
        # Loop through and add to a Song object with addNoteToTrack
        # For now default octave to 5, duration to eighth
        pass





if __name__ == '__main__':
    seq = NoteSequence('C', SOPRANO, 20)
    print(seq)
