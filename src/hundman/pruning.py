"""
NOTE: this follows my reading of the Figure 2 caption and the example in it.
The paragraph explaining the rule was not available, so check it against the
paper before trusting the details marked "DECISION".

Idea:
  1. For each flagged sequence, take its highest error (e_max).
  2. Sort these from highest to lowest.
  3. Add one more value at the end: the highest error that is NOT in any
     flagged sequence (the highest "normal" error).
  4. Look at the percent drop between neighbours:
         d(i) = (L[i-1] - L[i]) / L[i-1]
  5. A drop bigger than p is a clear gap, so the sequences above it stay flagged.
     If the drops are small (<= p), the sequences are too close to the normal
     errors and are reclassified as normal.

Caption example: e_max = [0.01396, 0.01072], highest normal error = 0.00994, p = 0.1
    d(1) = (0.01396 - 0.01072) / 0.01396 = 0.23  > p  -> keep
    d(2) = (0.01072 - 0.00994) / 0.01072 = 0.07  < p  -> reclassify as normal
"""
import numpy as np


def sequence_maxes(errors, sequences):
    """
    errors    : array of smoothed errors
    sequences : list of (start, end) pairs from sequences.py
    returns   : list of the highest error of each sequence (same order as sequences)
    """
    list = []
    # for each (start, end), take errors[start : end + 1] and its max
    for i in range(0, len(sequences)):
        list.append(max(errors[sequences[i][0] : sequences[i][1]+1]))

    # return the list
    return list


def highest_normal_error(errors, sequences):
    """
    returns : the highest error that is NOT inside any flagged sequence
    """
    # make a True/False array the length of errors, all True at first
    array = []
    for i in range(0, len(errors)):
        array.append(True)
    # for each (start, end), mark those positions as False (flagged)
    for s in sequences:
        for j in range(s[0], s[1] + 1):
            array[j] = False
    # return the max of the errors that are still True
    mx = 0
    for i in range(len(errors)):
        if array[i] == True and errors[i] > mx:
            mx = errors[i]
    return mx


def prune(errors, sequences, p=0.1):
    """
    errors    : array of smoothed errors
    sequences : list of (start, end) pairs
    p         : minimum percent drop (the paper uses 0.1)
    returns   : the list of sequences that stay flagged
    """
    # if there are no sequences, return an empty list
    if len(sequences) == 0 :
        return []

    # get the max of each sequence (sequence_maxes)
    maxes =  sequence_maxes(errors, sequences)
    # sort the sequences from highest max to lowest max (keep the pairs together)
    pairs = list(zip(maxes, sequences))
    pairs.sort(reverse=True)

    #  build the list L: the sorted maxes, then the highest normal error at the end
    L = []
    for p in pairs:
        L.append(p[0])
    L.append(highest_normal_error(errors, sequences))
    # compute the drops d(i) = (L[i-1] - L[i]) / L[i-1] for i = 1 ... len(L) - 1
    drops = []
    for i in range(1, len(L)):
        d = (L[i-1] - L[i]) / L[i-1]
        drops.append(d)

    #   which sequences stay flagged?
    #   My reading: find the LAST drop that is bigger than p.
    #   Every sequence above that drop stays flagged; the ones below it are dropped.
    #   If no drop is bigger than p, all sequences are dropped.
    LatDrop = None
    for d in drops:
        if d > p:
            LatDrop = d
    flags = []
    for i in range(0, errors):
        if errors[i] > d:
            flags.append(True)
        else:
            flags.append(False)




    # return the sequences that stay flagged
    pass


if __name__ == "__main__":
    # Check by hand (the caption example):
    errors = np.array([0.001, 0.01396, 0.002, 0.01072, 0.003, 0.00994, 0.002])
    sequences = [(1, 1), (3, 3)]
    # Expected: only (1, 1) stays flagged -> [(1, 1)]
    # call prune(errors, sequences, 0.1) and print the result
    pass
