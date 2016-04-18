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
    def __init__(self, msg='Invalid key.'):
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
        self.currentOctave = voice
        self.root = ''              # Set in the parseKey function
        self.keyDescription = ''
        self.parseKey(key)          # TODO: self.key = self.parseKey(key)
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

    # Markov Chain algorithm for generating a sequence of notes. Note choice is
    # decided in getNextNote(), this function merely organizes and houses then
    # overall logic.
    def generate(self):
        random.seed()           # For note probabilities
        seq = [Note(self.root, self.voice, EIGHTH, 20)] #Note(note, octave, duration, velocity)
        self.noteHistory.append(Note(self.root, self.voice, EIGHTH, 20))
        while len(seq) < self.length:
            newNote = self.getNextNote()
            seq.append(newNote)
            self.noteHistory.append(newNote)
        return seq

    # Sets NoteSequence.key = the array.
    #   Throws: InvalidKeyError if user defined key is not supported.
    def parseKey(self, key):
        tokens = key.split(' ', 1)
        self.root = tokens[0]
        self.keyDescription = tokens[1]
        key = self.defineKey(tokens[1:])
        if key is InvalidKeyError: raise InvalidKeyError
        else:
            i = 0
            for i in range(len(key)):
                #TODO: This might be where it's getting incremented
                key[i] = (self.getNoteValue(self.root) + key[i]) % 12
            self.key = key
            print(self.key)

    # Converts user specified key: 'C# Natural Minor' -> array of notes in key.
    #   Throws: InvalidKeyError if user defined key is not supported.
    def defineKey(self, token):
        case = {
            'major' : MAJOR_SCALE,
            'natural minor' : MINOR_SCALE_NATURAL,
            'harmonic minor' : MINOR_SCALE_HARMONIC
        }
        #TODO: MAJOR_SCALE is getting incremented somehow
        try: intervalList = case.get(str(token[0]).lower(), InvalidKeyError)
        except InvalidKeyError: raise InvalidKeyError
        return list(intervalList)

    def noteProbabilities(self, noteValue):
        chains = []
        # Root
        if noteValue == self.key[0]:
            chains = [0.05, 0.2, 0.4, 0.6, 0.8, 0.9, 1]
        # 2nd
        if noteValue == self.key[1]:
            chains = [0.05, 0.2, 0.4, 0.6, 0.8, 0.9, 1]
        # 3rd
        if noteValue == self.key[2]:
            chains = [0.05, 0.2, 0.4, 0.6, 0.8, 0.9, 1]
        # 4th
        if noteValue == self.key[3]:
            chains = [0.2, 0.4, 0.55, 0.6, 0.8, 0.95, 1]
        # 5th
        if noteValue == self.key[4]:
            chains = [0.05, 0.2, 0.4, 0.6, 0.8, 0.9, 1]
        # 6th
        if noteValue == self.key[5]:
            chains = [0.05, 0.2, 0.4, 0.65, 0.7, 0.8, 1]
        # 7th
        if noteValue == self.key[6]:
            chains = [0.4, 0.45, 0.55, 0.75, 0.85, 0.95, 1]
        return chains

    def getNextNote(self):
        chooser = random.random()

        # 10% chance to go down an octave
        if chooser < 0.1 and self.currentOctave >= self.voice:
            self.currentOctave = self.currentOctave - 1
        # 10% chance to go up an octave
        elif chooser < 0.2 and self.currentOctave <= self.voice:
            self.currentOctave = self.currentOctave + 1
        else:
            octave = self.currentOctave
        #Sets octave for next note
        octave = self.currentOctave

        # Probabilities for each interval
        chooser = random.random()
        probs = self.noteProbabilities(self.noteHistory[-1].noteValue)
        if chooser < probs[0]: note = self.key[0]
        elif chooser < probs[1]: note = self.key[1]
        elif chooser < probs[2]: note = self.key[2]
        elif chooser < probs[3]: note = self.key[3]
        elif chooser < probs[4]: note = self.key[4]
        elif chooser < probs[5]: note = self.key[5]
        elif chooser < probs[6]: note = self.key[6]

        # Probablities for each duration
        duration = SIXTEENTH
        # chooser = random.random()
        # if chooser < 0.15: duration = HALF
        # elif chooser < 0.3: duration = QUARTER
        # elif chooser < 0.5: duration = EIGHTH
        # else: duration = SIXTEENTH

        # Generate new note
        return Note(note, octave, duration)

    # Given a song object and track number, writes it's note sequence data to the
    # specified track within the song object.
    # TODO: This logic should be handled by the song object!
    def writeSequenceToTrack(self, song, trackNum):
        for note in self.sequence:
            song.addNoteToTrack(trackNum, note.letter, note.octave, note.duration)

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

if __name__ == '__main__':
    seq = NoteSequence('A Major', SOPRANO, 100)
    seq.writeSequenceToTrack()
