"""
Severity score of one sequence:
    s = (max(errors in the sequence) - threshold) / (mean + std)
    mean and std are taken over the whole window of errors
"""
import numpy as np
# from smoothing import ewma
# from threshold import score_threshold

def find_sequences(errors, threshold):
    """
    errors    : array of smoothed errors
    threshold : the cutoff from threshold.py
    returns   : list of (start, end) pairs, one per run of consecutive
                errors above the threshold (both positions included)
                example: [1, 1, 9, 10, 1, 8] with threshold 5 -> [(2, 3), (5, 5)]
                this means indez 2 to 3 are above threshold and also index 5
    """
    # an empty list for the sequences
    sequences = []
    # make a variable for where the current run started (nothing yet)
    startRun = None

    # if errors[i] is above the threshold and no run is open: save i as the start
    # if errors[i] is NOT above the threshold and a run is open:
    #     save (start, i - 1) and close the run

    for i in range(0, len(errors)):
        if ((errors[i] > threshold) and (startRun is None) ):
            startRun = i
        elif((errors[i] <= threshold) and (startRun is not None) ):
            sequences.append((startRun, i-1))
            startRun = None


    #  after the loop, if a run is still open, save (start, last position)
    if startRun is not None:
        sequences.append((startRun, len(errors)-1))

    # return the list
    return sequences


def severity_score(errors, sequence, threshold):
    """
    errors    : array of smoothed errors (the whole window)
    sequence  : one (start, end) pair
    threshold : the cutoff from threshold.py
    returns   : one number, the severity of that sequence
    """
    # cut out the errors from start to end (remember end is included)
    new_errors = errors[sequence[0] : sequence[1]+1]

    # take the maximum of that piece
    maxi =  max(new_errors)
    # subtract the threshold
    r = maxi - threshold
    # divide by (mean + std) of the whole window
    r2 = r/ (np.mean(errors) +np.std(errors))
    # return the result
    return r2


if __name__ == "__main__":
    # Check by hand: errors [1, 1, 9, 10, 1, 8] with threshold 5
    # find_sequences should give [(2, 3), (5, 5)]
    errors = [1, 1, 9, 10, 1, 8]
    threshold = 5
    # call find_sequences and print the result
    seq = find_sequences(errors, threshold)
    print(f"find sequence: {seq}")
    # call severity_score for each sequence and print the scores
    for s in seq:
        print(f"sevirity score: {severity_score(errors, s,threshold)}")
