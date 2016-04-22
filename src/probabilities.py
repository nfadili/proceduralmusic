from constants import *

# Algorithm for determing the next added note's duration.
# Prevents an odd number of consecutive 16th notes.
# Returns -> list of probabilities for [HALF, QUARTER, EIGHTH, SIXTEENTH]
def durationDecider(durationHistory):
    prev = durationHistory[-1]
    if prev == HALF:
        #TODO: Handle multiple occurences with different probs
        return [.35, .7, .9, 1]
    if prev == QUARTER:
        #TODO: handle multiple occurences with different probs
        return [.25, .6, .8, 1]

    if prev == EIGHTH:
        durSum = 0;
        i = -1
        while durationHistory[i] == EIGHTH:
            i -= 1
            durSum += 1
        if durSum % 5 == 0: return [.05, .2, .75, 1]        #[8, 8, 8, 8, 8]
        if durSum % 3 == 0: return [.1, .3, .8, 1]          #[8, 8, 8]
        if durSum % 2 == 0: return [.15, .4, .75, 1]        #[8, 8]
        else: return [.05, .3, .7, 1]                       #[?, 8]

    if prev == SIXTEENTH:
        durSum = 0;
        i = -1
        while durationHistory[i] == SIXTEENTH:
            i -= 1
            durSum += 1
        if durSum % 8 == 0: return [.2, .5, .75, 1]         #[16, 16, 16, 16, 16, 16, 16, 16]
        if durSum % 4 == 0: return [.1, .4, .65, 1]         #[16, 16, 16, 16]
        if durSum % 2 == 0: return [.05, .3, .6, 1]         #[16, 16]
        else: return [0, 0, 0, 1]                           #odd number of 16ths

# Holds probability logic for determing the next note from any given interval.
# Returns -> list of not probabilities for [root, 2nd, 3rd, 4th, 5th, 6th, 7th]
def firstOrderMarkovChain(key, noteHistory):
    interval = noteHistory[-1].noteValue
    # Root
    if interval == key[0]:
        return [0.05, 0.2, 0.40, 0.6, 0.8, 0.9, 1]
    # 2nd
    if interval == key[1]:
        return [0.1, 0.15, 0.35, 0.55, 0.7, 0.85, 1]
    # 3rd
    if interval == key[2]:
        return [0.1, 0.25, 0.3, 0.45, 0.65, 0.85, 1]
    # 4th
    if interval == key[3]:
        return [0.15, 0.3, 0.45, 0.5, 0.7, 0.85, 1]
    # 5th
    if interval == key[4]:
        return [0.2, 0.35, 0.5, 0.65, 0.7, 0.85, 1]
    # 6th
    if interval == key[5]:
        return [0.15, 0.3, 0.5, 0.7, 0.8, 0.85, 1]
    # 7th
    if interval == key[6]:
        return [0.2, 0.35, 0.5, 0.65, 0.8, 0.95, 1]

#TODO: Maybe do this
def secondOrderMarkovChain(key, noteHistory):
    prev = noteHistory[-1].noteValue
    nextPrev = noteHistory[-1].noteValue
    probs = []
    #Root and...
    if prev == key[0] and prevNext == key[0]:
        return [.05, .5, .4, .55, .7, .85, 1]
    if prev == key[0] and prevNext == key[1]:
        return [.1, .15, .45, .65, .75, .85, 1]
    if prev == key[0] and prevNext == key[2]:
        return [.05, .5, .4, .55, .7, .85, 1]
    if prev == key[0] and prevNext == key[3]:
        return []
    if prev == key[0] and prevNext == key[4]:
        return []
    if prev == key[0] and prevNext == key[5]:
        return []
    if prev == key[0] and prevNext == key[6]:
        return []

    #2nd and...
    if prev == key[1] and prevNext == key[0]:
        return []
    if prev == key[1] and prevNext == key[1]:
        return []
    if prev == key[1] and prevNext == key[2]:
        return []
    if prev == key[1] and prevNext == key[3]:
        return []
    if prev == key[1] and prevNext == key[4]:
        return []
    if prev == key[1] and prevNext == key[5]:
        return []
    if prev == key[1] and prevNext == key[6]:
        return []

    #3nd and...
    if prev == key[2] and prevNext == key[0]:
        return []
    if prev == key[2] and prevNext == key[1]:
        return []
    if prev == key[2] and prevNext == key[2]:
        return []
    if prev == key[2] and prevNext == key[3]:
        return []
    if prev == key[2] and prevNext == key[4]:
        return []
    if prev == key[2] and prevNext == key[5]:
        return []
    if prev == key[2] and prevNext == key[6]:
        return []

    #4th and...
    if prev == key[3] and prevNext == key[0]:
        return []
    if prev == key[3] and prevNext == key[1]:
        return []
    if prev == key[3] and prevNext == key[2]:
        return []
    if prev == key[3] and prevNext == key[3]:
        return []
    if prev == key[3] and prevNext == key[4]:
        return []
    if prev == key[3] and prevNext == key[5]:
        return []
    if prev == key[3] and prevNext == key[6]:
        return []

    #5th and...
    if prev == key[4] and prevNext == key[0]:
        return []
    if prev == key[4] and prevNext == key[1]:
        return []
    if prev == key[4] and prevNext == key[2]:
        return []
    if prev == key[4] and prevNext == key[3]:
        return []
    if prev == key[4] and prevNext == key[4]:
        return []
    if prev == key[4] and prevNext == key[5]:
        return []
    if prev == key[4] and prevNext == key[6]:
        return []

    #6th and...
    if prev == key[5] and prevNext == key[0]:
        return []
    if prev == key[5] and prevNext == key[1]:
        return []
    if prev == key[5] and prevNext == key[2]:
        return []
    if prev == key[5] and prevNext == key[3]:
        return []
    if prev == key[5] and prevNext == key[4]:
        return []
    if prev == key[5] and prevNext == key[5]:
        return []
    if prev == key[5] and prevNext == key[6]:
        return []

    #7th and...
    if prev == key[6] and prevNext == key[0]:
        return []
    if prev == key[6] and prevNext == key[1]:
        return []
    if prev == key[6] and prevNext == key[2]:
        return []
    if prev == key[6] and prevNext == key[3]:
        return []
    if prev == key[6] and prevNext == key[4]:
        return []
    if prev == key[6] and prevNext == key[5]:
        return []
    if prev == key[6] and prevNext == key[6]:
        return []
