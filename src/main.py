from Song import *
from NoteSequence import *
from MidiNote import *

def initialSongUI():
    trackCount = raw_input('Enter track count: ')
    tempo = raw_input('Enter a tempo: ')
    key = raw_input('Enter a key: ')
    length = raw_input('Enter a song length: ')
    return (int(trackCount), int(tempo), str(key), str(length))

#Supports up to four tracks
#TODO: Make this a little more elegant
def determineVoice(currentTrackCount):
    if currentTrackCount == 0: return ALTO
    if currentTrackCount == 1: return BASS
    if currentTrackCount == 2: return SOPRANO
    if currentTrackCount == 3: return TENOR

if __name__ == '__main__':
    choices = initialSongUI()
    song = Song(choices[0],         #Track Count
                choices[1])         #Tempo
    key = choices[2]                #Key
    length = int(choices[3])        #Length
    for i in range(song.trackCount):
        seq = NoteSequence(key, determineVoice(i), length)
        seq.writeSequenceToTrack(song, i)

    song.markSongEnd()
    midi.write_midifile("example.mid", song.pattern)
