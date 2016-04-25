from random import randint
from constants import *
from Note import *

class Motifs:
    def __init__(self, motifFile):
        #TODO: Differentiate between pickle and text files to call correct function
        self.fixedMotifs = self.parseTextFile(motifFile)
        self.generatedMotifs = []

    # Text file format -> IntervalDuration, IntervalDuration, ...
    # Returns list of lists of Notes
    def parseTextFile(self, motifFile):
        f = open(motifFile, 'r')
        motifList = []
        for line in f:
            seq = line.split(', ')
            motif = []
            octave = randint(2, 7)
            for note in seq:
                motif.append(Note(int(note[0]), octave, self.getDurationValue(note[1])))
            motifList.append(motif)
        return motifList

    def parsePickledFile(self, motifFile):
        pass

    def getDurationValue(self, letter):
        case = {
            'W' : WHOLE,
            'H' : HALF,
            'Q' : QUARTER,
            'E' : EIGHTH,
            'S' : SIXTEENTH
            'T' : THIRTY_SECOND,
            'F' : SIXTY_FOURTH
        }
        return case.get(letter)

if __name__ == '__main__':
    test = Motifs('db/motif_text_db.txt')
