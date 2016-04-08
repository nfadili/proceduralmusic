from Song import *
from constants import *
import random
from pprint import pprint

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
        if type(letter) is str: self.letter = letter
        elif type(letter) is int: self.letter = self.getNoteLetter(letter)
        self.octave = octave
        self.duration = duration
        self.velocity = velocity
        self.noteValue = self.getNoteValue(self.letter)
        #print(self.noteValue)

    def __str__(self):
        return '(' + self.letter + ', ' + str(self.octave) + ', ' + str(self.duration)\
               + ', ' + str(self.velocity) + ')'

    def getNoteValue(self, note):
        case = {
            'C' : 0,
            'C#' : 1,
            'D' : 2,
            'D#' : 3,
            'E' : 4,
            'F' : 5,
            'F#' : 6,
            'G' : 7,
            'G#' : 8,
            'A' : 9,
            'A#' : 10,
            'B' : 11
        }
        return case.get(note)
    def getNoteLetter(self, value):
        case = {
            0 : 'C',
            1 : 'C#',
            2 : 'D',
            3 : 'D#',
            4 : 'E',
            5 : 'F',
            6 : 'F#',
            7 : 'G',
            8 : 'G#',
            9 : 'A',
            10 : 'A#',
            11 : 'B'
        }
        return case.get(value)

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
        string = 'Key: ' + self.root + ' ' + self.keyDescription + ' '\
                 + str(self.key) + '\n' + case.get(self.voice) + '\n['
        for note in self.sequence:
            string += str(note)
        return string + ']'

    def generate(self):
        random.seed()           # For note probabilities
        seq = [Note(self.root, self.voice, EIGHTH, 20)] #Note(note, octave, duration, velocity)
        self.noteHistory.append(Note(self.root, self.voice, EIGHTH, 20))
        while len(seq) < self.length:
            seq.append(Note(self.root, self.voice, EIGHTH, 20))
            newNote = self.getNextNote()
            seq.append(newNote)
            self.noteHistory.append(newNote)
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
        # 5% chance to go up an octave, %5 chance to go down an octave
        chooser = random.random()
        if chooser < 0.05:
            octave = self.voice - 1
        elif chooser < 0.1:
            octave = self.voice + 1
        else:
            octave = self.voice

        # Probabilities for each interval
        chooser = random.random()
        if chooser < 0.125: note = (self.noteHistory[-1].noteValue + self.key[0]) % 12
        elif chooser < 0.25: note = (self.noteHistory[-1].noteValue + self.key[1]) % 12
        elif chooser < 0.375: note = (self.noteHistory[-1].noteValue + self.key[2]) % 12
        elif chooser < 0.5: note = (self.noteHistory[-1].noteValue + self.key[3]) % 12
        elif chooser < 0.625: note = (self.noteHistory[-1].noteValue + self.key[4]) % 12
        elif chooser < 0.75: note = (self.noteHistory[-1].noteValue + self.key[5]) % 12
        elif chooser < 0.875: note = (self.noteHistory[-1].noteValue + self.key[6]) % 12
        else: note = (self.noteHistory[-1].noteValue + self.key[7]) % 12

        # Probablities for each duration
        chooser = random.random()
        if chooser < 0.25: duration = HALF
        elif chooser < 0.5: duration = QUARTER
        elif chooser < 0.75: duration = EIGHTH
        else: duration = SIXTEENTH

        # Generate new note
        return Note(note, octave, duration)

    def writeSequenceToTrack(self):
        song = Song(1, 120)
        for note in self.sequence:
            song.addNoteToTrack(0, note.letter, note.octave, note.duration)
        song.markSongEnd()
        midi.write_midifile("example.mid", song.pattern)

if __name__ == '__main__':
    seq = NoteSequence('C Major', SOPRANO, 50)
    seq.writeSequenceToTrack()
