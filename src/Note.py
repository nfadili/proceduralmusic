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
