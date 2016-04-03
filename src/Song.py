import midi
from Note import *
from constants import *

class Song:
    # Reference to tracks are immedietly added to the midi.Pattern object.
    def __init__(self, numTracks):
        self.pattern = midi.Pattern(resolution=MIDI_RESOLUTION)
        self.track = []
        for i in range(numTracks):
            self.track.append(midi.Track())
            self.pattern.append(self.track[i])

    def addNoteToTrack(self, trackNum, note, octave, duration, vel=20):
        note = str(note) + '_' + str(octave)
        note = newNote(note, duration, vel)
        self.track[trackNum].append(note[0])
        self.track[trackNum].append(note[1])

    # Appends a midi event to mark the end of a track to all tracks in the song.
    # Must be called before writing the midi data to a file.
    def markSongEnd(self):
        eot = midi.EndOfTrackEvent(tick=1)
        for track in self.track:
            track.append(eot)


if __name__ == '__main__':
    song = Song(2)

    song.addNoteToTrack(0, 'A', 4, 4)
    song.addNoteToTrack(0, 'C', 5, 8)
    song.addNoteToTrack(0, 'D', 5, 8)
    song.addNoteToTrack(0, 'E', 5, 4)
    song.addNoteToTrack(1, 'C', 5, 4)
    song.addNoteToTrack(1, 'E', 5, 4)
    song.addNoteToTrack(1, 'C', 6, 4)

    song.markSongEnd()
    print(song.pattern)
    midi.write_midifile("example.mid", song.pattern)
