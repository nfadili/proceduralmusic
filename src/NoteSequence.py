from Song import *
from Note import *
from constants import *
from Motifs import *
import probabilities
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
# NoteSequence class
################################################################################
# This class enforces music theory rules while generating sequences of notes for
# insertion into a Song object. Sequences are inserted into individual tracks within
# the Song object.
class NoteSequence:

    def __init__(self, key, voice, sequenceLength):
        self.motifs = Motifs('db/motif_text_db.txt').fixedMotifs    #Pass file for loading
        self.length = sequenceLength
        self.voice = voice          # Determines starting octave
        self.currentOctave = voice
        self.root = ''              # Set in the parseKey function
        self.keyDescription = ''
        self.parseKey(key)          # TODO: self.key = self.parseKey(key)
        self.noteHistory = []       # List of previous note values
        self.durationHistory = []   # List of previous note durations
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
        seq = [Note(self.root, self.voice, QUARTER, 20)] #Note(note, octave, duration, velocity)
        self.noteHistory.append(Note(self.root, self.voice, QUARTER, 20))
        self.durationHistory.append(QUARTER)    #TODO: Hard coding a starting duration is ugly!
        while len(seq) < self.length:           #      QUARTER IS NEEDED FOR THE ALGORITHM TO WORK
            newNote = self.getNextNote()
            seq.append(newNote)
            if (len(seq) % random.randint(1, 5) == 0 and self.checkDurationHistory()):
                self.getMotif(seq)
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
                key[i] = (self.getNoteValue(self.root) + key[i]) % 12
            self.key = key

    # Converts user specified key: 'C# Natural Minor' -> array of notes in key.
    #   Throws: InvalidKeyError if user defined key is not supported.
    def defineKey(self, token):
        case = {
            'major' : MAJOR_SCALE,
            'natural minor' : MINOR_SCALE_NATURAL,
            'harmonic minor' : MINOR_SCALE_HARMONIC
            #TODO: Add more scales
        }
        try: intervalList = case.get(str(token[0]).lower(), InvalidKeyError)
        except InvalidKeyError: raise InvalidKeyError
        return list(intervalList)

    # Determines next note to added by calling helper algorithms for
    # the note value and duration. Octave is dtermined randomly in the range
    # of +1 or -1.
    def getNextNote(self):
        chooser = random.random()

        # 10% chance to go down an octave
        if chooser < 0.1 and self.currentOctave >= self.voice:
            self.currentOctave = self.currentOctave - 1
        # 10% chance to go up an octave
        elif chooser < 0.2 and self.currentOctave <= self.voice:
            self.currentOctave = self.currentOctave + 1
        #Sets octave for next note
        octave = self.currentOctave

        # Probabilities for each interval
        chooser = random.random()
        #First order markov chain
        probs = probabilities.firstOrderMarkovChain(self.key, self.noteHistory)
        if chooser < probs[0]: note = self.key[0]
        elif chooser < probs[1]: note = self.key[1]
        elif chooser < probs[2]: note = self.key[2]
        elif chooser < probs[3]: note = self.key[3]
        elif chooser < probs[4]: note = self.key[4]
        elif chooser < probs[5]: note = self.key[5]
        elif chooser <= probs[6]: note = self.key[6]

        # Probablities for each duration
        chooser = random.random()

        #Duration algorithm probabilities
        probs = probabilities.durationDecider(self.durationHistory)

        if chooser < probs[0]:
            duration = HALF
            self.durationHistory.append(HALF)
        elif chooser < probs[1]:
            duration = QUARTER
            self.durationHistory.append(QUARTER)
        elif chooser < probs[2]:
            duration = EIGHTH
            self.durationHistory.append(EIGHTH)
        elif chooser <= probs[3]:
            duration = SIXTEENTH
            self.durationHistory.append(SIXTEENTH)

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

    def getMotif(self, seq):
        motif = self.motifs[random.randint(0, len(self.motifs)-1)]
        for note in motif:
            noteInKey = self.key[note[0]]
            duration = int(note[1])
            seq.append(Note(self.key[note[0]], self.currentOctave, int(note[1])))
            self.durationHistory.append(duration)
            self.noteHistory.append(noteInKey)

    def checkDurationHistory(self):
        firstNote = self.durationHistory[-1]
        if firstNote is SIXTEENTH:
            count = 0
            i = -1
            while(self.durationHistory[i] is SIXTEENTH):    # Might check out of bounds if quarter note isnt the first note
                count += 1
                i -= 1
            if count % 2 == 0: return True
            else : return False
        else:
            return True

if __name__ == '__main__':
    # TESTING
    seq = NoteSequence('A Major', SOPRANO, 100)
    seq.writeSequenceToTrack()
