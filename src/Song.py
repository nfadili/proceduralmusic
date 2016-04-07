import midi
from MidiNote import *
from constants import *

class Song:
    # Reference to tracks are immedietly added to the midi.Pattern object.
    def __init__(self, numTracks, tempo=120):
        self.globalTickCount = 0
        self.startTempo = tempo
        self.pattern = midi.Pattern(resolution=MIDI_RESOLUTION)
        self.pattern.append([])                 # Add initial track for tempo changes
        self.addTempoEvent(tempo)               # Add initial tempo
        self.track = []
        for i in range(numTracks):
            self.track.append(midi.Track())
            self.pattern.append(self.track[i])

    # Interfaces with the Note.py file to add a note to a designated track in the song.
    def addNoteToTrack(self, trackNum, note, octave, duration, vel=20):
        self.globalTickCount += parseDuration(duration)[1]      # Duration of note is added to global count
        note = str(note) + '_' + str(octave)
        note = newNote(note, duration, vel)
        self.track[trackNum].append(note[0])    # midi on event
        self.track[trackNum].append(note[1])    # midi off event

    # Interfaces with the Note.py file to add a rest to a designated track in the song.
    def addRestToTrack(self, trackNum, duration):
        self.globalTickCount += parseDuration(duration)[1]      # Duration of rest is added to global count
        rest = newRest(duration)
        self.track[trackNum].append(rest[0])    # rests require only midi on event. (NOTE check this)

    # Appends a midi event to mark the end of a track to all tracks in the song.
    # Must be called before writing the midi data to a file.
    def markSongEnd(self):
        eot = midi.EndOfTrackEvent(tick=1)
        self.addTempoEvent(self.startTempo)
        self.pattern[0].append(eot)
        for track in self.track:
            track.append(eot)

    # Adds a tempo event to the midi track at the current (relative) tick of the song.
    # Current tick is specified with self.globalTickCount
    def addTempoEvent(self, tempo):
        self.pattern[0].append(midi.SetTempoEvent(tick=self.globalTickCount, data=self.parseTempoData(tempo)))

    # Formats a given integer tempo into -> data[hex1, hex2, hex3].
    # Must be called when midi.SetTempoEvent is called
    def parseTempoData(self, tempo):
        hexString = hex(MICROSECONDS_PER_MINUTE / tempo)    # calculates microseconds per beat
        digits = []
        i = len(hexString)
        while i > 1:
            digits.insert(0, hexString[i-2:i])              # parse string from back, 2 at a time
            i -= 2
        if 'x' in digits[0]: digits[0] = digits[0][1:2]     # remove python's 'x' hex syntax
        data = []
        for digit in digits:
            data.append(int(digit, 16))
        return data

if __name__ == '__main__':
    song = Song(2, 180)
    song.addNoteToTrack(0, 'A', 4, QUARTER)
    song.addNoteToTrack(0, 'C', 5, HALF)
    song.addNoteToTrack(0, 'E', 4, HALF)
    song.addTempoEvent(120)
    song.addNoteToTrack(0, 'C', 4, HALF)
    song.addTempoEvent(80)
    song.addNoteToTrack(0, 'A', 4, QUARTER)
    song.addNoteToTrack(0, 'C', 5, HALF)
    song.addNoteToTrack(0, 'E', 4, HALF)
    song.addNoteToTrack(0, 'C', 4, HALF)
    song.addTempoEvent(100)
    song.addNoteToTrack(0, 'A', 4, QUARTER)
    song.addNoteToTrack(0, 'C', 5, HALF)
    song.addNoteToTrack(0, 'E', 4, HALF)
    song.addNoteToTrack(0, 'C', 4, HALF)
    song.addNoteToTrack(0, 'C', 4, HALF)
    # song.addNoteToTrack(1, 'A', 4, QUARTER)
    # song.addNoteToTrack(1, 'C', 5, HALF)
    # song.addNoteToTrack(1, 'E', 4, HALF)
    # song.addNoteToTrack(1, 'C', 4, HALF)
    # song.addRestToTrack(1, QUARTER)
    # song.addRestToTrack(1, QUARTER)
    # song.addRestToTrack(1, QUARTER)
    # song.addNoteToTrack(1, 'C', 4, HALF)


    song.markSongEnd()
    print(song.pattern)
    midi.write_midifile("example.mid", song.pattern)

################################################################################
# Exception definitions
################################################################################
class SongError(Exception):
    # Base class for Song errors.
    pass

class TempoError(SongError):
    def __init__(self, msg):
        self.msg = msg
