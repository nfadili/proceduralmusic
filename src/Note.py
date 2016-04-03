import midi


# Add self to param list if you end up making a class/API
# Parse to -> data[NOTE, VELOCITY]
def newNote(pitch, duration, vel=20):
    noteVal = parsePitch(pitch)
    ticks = parseDuration(duration)
    on = midi.NoteOnEvent(tick=ticks[0], velocity=vel, pitch=noteVal)
    off = midi.NoteOffEvent(tick=ticks[1], pitch=noteVal)
    return (on, off)

# Format must follow -> LETTER(ACCIDENTAL)_OCTAVE
# Returns MIDI value (int) associated with the note or -1 if a rest
def parsePitch(pitch):
    if pitch == 'R': return -1
    note, octave = pitch.split('_')
    if int(octave) > 8 or int(octave) < 0: raise PitchError('Octave out of range: [0, 8].')
    if len(note) is 2: note, acc = note
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

# Takes in a standard note duration:
#   whole = 1
#   half = 2
#   quarter = 4
#   eighth = 8
#   sixteenth = 16
#   thirty-second = 32
#   sixty-fourth = 64
# Returns tuple (startTick, endTick) for parsing in the newNote function
def parseDuration(duration):
    case= {
        1 : 64,
        2 : 32,
        4 : 16,
        8 : 8,
        16: 4,
        32: 2,
        64: 1
    }
    startTick = 0
    endTick = case.get(duration)
    return (startTick, endTick)

if __name__ == '__main__':
    pattern = midi.Pattern(resolution=16)
    track = midi.Track()
    pattern.append(track)

    note = newNote('C_5', 16, 20)
    track.append(note[0])   # midi.on event
    track.append(note[1])   #midi.off event

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)
    print(pattern)
    midi.write_midifile("example.mid", pattern)


################################################################################
# Exception definitions
################################################################################
class NoteError(Exception):
    # Base class for Note errors.
    pass

class PitchError(NoteError):
    def __init__(self, msg):
        self.msg = msg
