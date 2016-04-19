def firstOrderMarkovChain(key, interval):
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
