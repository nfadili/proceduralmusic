from Song import *
from Note import *
from constants import *
from Motifs import *
import probabilities
import random

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
        self.motifs = self.loadMotifs(voice)    #Loads matching voice file
        self.passages = []                      # Holds previously generated chunks of music
        self.length = sequenceLength
        self.voice = voice                      # Determines starting octave
        self.currentOctave = voice
        self.root = ''                          # Set in the parseKey function
        self.keyDescription = ''
        self.parseKey(key)                      # TODO: self.key = self.parseKey(key)
        self.noteHistory = []                   # List of previous note values
        self.durationHistory = []               # List of previous note durations
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

            #Potentially save a passage thats been generated.
            self.determineToSavePassage()

            # Check if its time to insert a passage
            print(len(self.passages))
            if (len(self.passages) is not 0 and len(seq) % 4 is 0):
                self.addPassageToTrack()
            # Determines how often to insert a motif
            if self.determineToAddMotif(len(seq)):
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
            'minor' : MINOR_SCALE_NATURAL,
            'harmonic minor' : MINOR_SCALE_HARMONIC,
            'gypsy' : GYPSY_SCALE,
            'neopolitan' : MAJOR_SCALE_NEOPOLITAN,
            'flamenco' : FLAMENCO_SCALE
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

    def loadMotifs(self, voice):
        case = {
            BASS : 'db/motif_text_db_bass.txt',
            TENOR : 'db/motif_text_db_tenor.txt',
            ALTO : 'db/motif_text_db_alto.txt',
            SOPRANO : 'db/motif_text_db_soprano.txt'
        }
        return Motifs(case.get(voice)).fixedMotifs

    def getMotif(self, seq):
        motif = self.motifs[random.randint(0, len(self.motifs)-1)]
        for note in motif:
            noteInKey = self.key[note[0]]
            duration = int(note[1])
            seq.append(Note(self.key[note[0]], self.currentOctave, int(note[1])))
            self.durationHistory.append(duration)
            self.noteHistory.append(noteInKey)

    # Determines the frequency of adding from the motif db. The lower the mod amount
    # the more often a motif is inserted.
    def determineToAddMotif(self, count):
        if self.voice is SOPRANO:
            return (count % 10 == 0 and self.checkDurationHistory())
        if self.voice is TENOR:
            return (count % 8 == 0 and self.checkDurationHistory())
        if self.voice is ALTO:
            return (count % 6 == 0 and self.checkDurationHistory())
        if self.voice is BASS:
            return (count % 4 == 0 and self.checkDurationHistory())

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

    def addPassageToTrack(self):
        passage = self.findPassage()
        for note in passage:
            self.seq.append(note)
            self.noteHistory.append(note)
            self.durationHistory.append(note.duration)
        print("Added Passage!")
        print(passage)

    def savePassage(self):
        measureCount = 0
        lookbackCounter = -2
        newPassage = []
        newPassage.append(self.noteHistory[-1])
        measureCount += self.noteHistory[-1].duration
        while measureCount % MIDI_WHOLE is not 0:
            newPassage.append(self.noteHistory[lookbackCounter])
            measureCount += self.noteHistory[lookbackCounter].duration
            lookbackCounter -= 1
        self.passages.append(newPassage.reverse())
        print("Saved Passage!")
        print(self.passages[0])
        print(newPassage)
        print(self.passages[0])

    def findPassage(self):
        print("Found Passage!")
        return self.passages[random.randint(0, len(self.passages))]

    def determineToSavePassage(self):
        count = 0
        lookbackCounter = -1
        while count % MIDI_WHOLE is not 0 or lookbackCounter < len(self.noteHistory) * -1:
            lookbackCounter -= 1
            print(lookbackCounter)
            print(len(self.noteHistory))
            count += self.noteHistory[lookbackCounter].duration
        if count % MIDI_WHOLE is 0:
            self.savePassage()


if __name__ == '__main__':
    # TESTING
    seq = NoteSequence('A Major', SOPRANO, 100)
    seq.writeSequenceToTrack()
