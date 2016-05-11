# MIDI variables #
MIDI_RESOLUTION = 16

# Conversion of standard note durations to resolution based durations #
MIDI_WHOLE = MIDI_RESOLUTION * 4
MIDI_HALF = MIDI_RESOLUTION * 2
MIDI_QUARTER = MIDI_RESOLUTION
MIDI_EIGHTH = int(MIDI_RESOLUTION * 0.5)
MIDI_SIXTEENTH = int(MIDI_RESOLUTION * 0.25)
MIDI_THIRTY_SECOND = int(MIDI_RESOLUTION * 0.125)
MIDI_SIXTY_FOURTH = int(MIDI_RESOLUTION * 0.0625)

# Assumed note duration format #
WHOLE = 1
HALF = 2
QUARTER = 4
EIGHTH = 8
SIXTEENTH = 16
THIRTY_SECOND = 32
SIXTY_FOURTH = 64

# Constants #
MICROSECONDS_PER_MINUTE = 60000000

# Music Theory Rules #
MIN_OCTAVE = 1
MAX_OCTAVE = 8
NOTES_IN_OCTAVE = 12

# Algorithm Rules
PASSAGE_LENGTH = 4
PASSAGE_RATIO = 4

# Voice Ranges (Octave lies midway through the voice range) #
BASS = 3
TENOR = 4
ALTO = 5
SOPRANO = 6

# Steps #
HALF = 1
WHOLE = 2
WHOLE_HALF = 3

# Intervals #

# Octave 1
P1 = 0
m2 = HALF
M2 = WHOLE
m3 = M2 + HALF
M3 = m3 + HALF
P4 = M3 + HALF
TT = P4 + HALF
P5 = TT + HALF
m6 = P5 + HALF
M6 = m6 + HALF
m7 = M6 + HALF
M7 = m7 + HALF

# Octave 2
P8 = 12
m9 = P8 + HALF
M9 = m9 + HALF
m10 = M9 + HALF
M10 = m10 + HALF
P11 = M10 + HALF
CT = P11 + HALF     # Compound Tritone
P12 = CT + HALF
m13 = P12 + HALF
M13 = m13 + HALF
m14 = M13 + HALF
M14 = m14 + HALF
P15 = 24

# Scales #
MAJOR_SCALE = [0, M2, M3, P4, P5, M6, M7]
MAJOR_SCALE_NEOPOLITAN = [0, m2, m3, P4, P5, M6, M7]
MINOR_SCALE_NATURAL = [0, M2, m3, P4, P5, m6, m7]
MINOR_SCALE_HARMONIC = [0, M2, m3, P4, P5, m6, M7]
FLAMENCO_SCALE = [0, m2, M3, P4, P5, m6, M7]
GYPSY_SCALE = [0, M2, m3, TT, P5, m6, m7]
