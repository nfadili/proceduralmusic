from Song import *
from NoteSequence import *
from MidiNote import *

def initialSongUI():
    trackCount = raw_input('Enter track count: ')
    tempo = raw_input('Enter a tempo: ')
    key = raw_input('Enter a key: ')
    return (int(trackCount), int(tempo), str(key))

if __name__ == '__main__':
    choices = initialSongUI()
    song = Song(choices[0],         #Track Count
                choices[1])         #Tempo
    key = choices[2]                #Key
    for i in range(song.trackCount):
        seq = NoteSequence(key, SOPRANO, 100)
        seq.writeSequenceToTrack(song, i)

    song.markSongEnd()
    midi.write_midifile("example.mid", song.pattern)
