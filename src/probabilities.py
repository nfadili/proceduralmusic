from constants import *

def durationDecider(durationHistory):
    prev = durationHistory[-1]

    if prev == HALF:
        return [.35, .7, .9, 1]
    if prev == QUARTER:
        return [.25, .6, .8, 1]
    if prev == EIGHTH:
        if durationHistory[-2] == EIGHTH:
            return [.25, .5, .75, 1]
        else:
            return [.05, .3, .7, 1]
    if prev == SIXTEENTH:
        if durationHistory[-2] is not SIXTEENTH:        #[?, ?, ?, 16]
            return [0, 0, 0, 1]
        else:
            if durationHistory[-3] is not SIXTEENTH:    #[?, ?, 16, 16]
                return [.05, .3, .6, 1]
            else:
                if durationHistory[-4] is not SIXTEENTH:#[?, 16, 16, 16]
                    return [0, 0, 0, 1]
                else:                                   #[16, 16, 16, 16]
                    return [.2, .4, .6, 1]

def firstOrderMarkovChain(key, noteHistory):
    interval = noteHistory[-1].noteValue
    probs = []
    # Root
    if interval == key[0]:
        probs = [0.05, 0.2, 0.40, 0.6, 0.8, 0.9, 1]
    # 2nd
    if interval == key[1]:
        probs = [0.1, 0.15, 0.35, 0.55, 0.7, 0.85, 1]
    # 3rd
    if interval == key[2]:
        probs = [0.1, 0.25, 0.3, 0.45, 0.65, 0.85, 1]
    # 4th
    if interval == key[3]:
        probs = [0.15, 0.3, 0.45, 0.5, 0.7, 0.85, 1]
    # 5th
    if interval == key[4]:
        probs = [0.2, 0.35, 0.5, 0.65, 0.7, 0.85, 1]
    # 6th
    if interval == key[5]:
        probs = [0.15, 0.3, 0.5, 0.7, 0.8, 0.85, 1]
    # 7th
    if interval == key[6]:
        probs = [0.2, 0.35, 0.5, 0.65, 0.8, 0.95, 1]
    return probs

def secondOrderMarkovChain(key, noteHistory):
    prev = noteHistory[-1].noteValue
    nextPrev = noteHistory[-1].noteValue
    probs = []
    #Root and...
    if prev == key[0] and prevNext == key[0]:
        return []
    if prev == key[0] and prevNext == key[1]:
        return []
    if prev == key[0] and prevNext == key[2]:
        return []
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
