import Song
from constants import *

################################################################################
# Exception definitions
################################################################################
class NoteSequenceError(Exception):
    pass

class InvalidKeyError(NoteSequenceError):
    def __init__(self, msg):
        self.msg = msg

################################################################################
# Inner class
################################################################################
class Note:
    def __init__(self, letter, octave, duration, velocity=20):
         self.letter = letter
         self.octave = octave
         self.duration = duration
         self.velocity = velocity

    def __str__(self):
        return '(' + self.letter + str(self.octave) + ', ' + str(self.duration) + ', ' + str(self.velocity) + ')'

################################################################################
# NoteSequence class
################################################################################
# This class enforces music theory rules while generating sequences of notes for
# insertion into a Song object. Sequences are inserted into individual tracks within
# the Song object.
class NoteSequence:

    def __init__(self, key, voice, sequenceLength):
        self.length = sequenceLength
        self.voice = voice          # Determines starting octave
        self.root = ''              # Set in the parseKey function
        self.keyDescription = ''
        self.key = self.parseKey(key)
        self.noteHistory = []       # Start with only previous note, then look back farther. (Higher order markov chain).
        self.sequence = self.generate()

    def __str__(self):
        case = {
            2 : 'BASS',
            3 : 'TENOR',
            4 : 'ALTO',
            5 : 'SOPRANO'
        }
        string = 'Key: ' + self.root + ' '+ self.keyDescription + '\n' + case.get(self.voice) + '\n['
        for note in self.sequence:
            string += str(note)
        return string + ']'

    def generate(self):
        seq = [Note(self.root, self.voice, EIGHTH, 20)] #Note(root, octave, duration, velocity)
        while len(seq) < self.length:
            seq.append(Note(self.root, self.voice, EIGHTH, 20))
            # newNote = self.getNextNote()
            # seq.append(newNote)
            # self.noteHistory.append(newNote.letter)
        return seq

    def parseKey(self, key):
        tokens = key.split(' ', 1)
        self.root = tokens[0]
        self.keyDescription = tokens[1]
        key = self.defineKey(tokens[1:])
        if key is not InvalidKeyError: return key
    else: return None       # Throw error here or maybe later


    def defineKey(self, token):
        case = {
            'major' : MAJOR_SCALE,
            'natural minor' : MINOR_SCALE_NATURAL,
            'harmonic minor' : MINOR_SCALE_HARMONIC
        }
        return case.get(str(token[0]).lower(), InvalidKeyError('Invalid key.'))

    def getNextNote(self):
        return None

    def writeSequenceToTrack(self):
        # Loop through and add to a Song object with addNoteToTrack
        # For now default octave to 5, duration to eighth
        pass


if __name__ == '__main__':
    seq = NoteSequence('C# Major', SOPRANO, 20)
    print(seq)
