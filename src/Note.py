# Add self to param list if you end up making a class/API
# Parse to -> data[NOTE, VELOCITY]
def newNote(pitch, duration, velocity=20):
    noteVal = parsePitch(pitch)

# Format must follow -> LETTER(ACCIDENTAL)_OCTAVE
# Returns MIDI value (int) associated with the note or -1 if a rest
def parsePitch(pitch):
    if pitch == 'R': return -1
    note, octave = pitch.split('_')
    if len(note) is 2:note, acc = note
    else: acc = 0
    case= {
         0 : 0,
        '#': 1,
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11
    }
    return ((int(octave) * 12) + case.get(note) + case.get(acc))

################################################################################
# Tests
print parsePitch('C#_5')  #assert = 61
print parsePitch('C_5') #assert = 60
print parsePitch('D_3') #assert = 38
print parsePitch('D#_3') #assert = 39
print parsePitch('E_3') #assert = 40
print parsePitch('E#_3') #assert = 41
print parsePitch('R')     #assert = 0 or -1
