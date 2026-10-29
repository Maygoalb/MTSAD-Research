"""
Candidate threshold:
    eps = mean(window) + z * std(window)

Score of a candidate:
    score = (delta_mean / mean + delta_std / std) / (n_above + n_sequences ** 2)

    delta_mean  = mean(window) - mean(values below eps)
    delta_std   = std(window)  - std(values below eps)
    n_above     = number of values above eps
    n_sequences = number of separate runs of consecutive values above eps
"""
import numpy as np
import statistics


def count_sequences(above):
    """
    above  : array of True/False, True where a value is above the cutoff
    returns: number of separate runs of consecutive True values
             (example: [F, T, T, F, T] -> 2)
    """
    # count how many times a run of True values starts
    # (a run starts where above[i] is True and the previous one is False)

    # if the first is true then counting hsould start from index 1
    if (above[0] == True):
        n = 1
        count = 1
    else:
        n = 0
        count = 0
    for i in range(n, len(above)):
        if ((above[i] == True) and (above[i-1] == False)):
            count += 1
    return count

def candidate_thresholds(window, z_values):
    """
    window   : array of smoothed errors
    z_values : list of z multipliers to try (the paper says about 2 to 10)
    returns  : list of candidate cutoffs, one per z
    """
    # compute mean and std of the window
    sum = 0
    for i in window:
        sum += i
    mean =  sum / len(window)
    #  for each z, compute mean + z * std
    cutoff = []
    for z in range(0, len(z_values)):
        r = mean + (z_values[z] * statistics.stdev(window))
        cutoff.append(r)

    # return the list
    return cutoff


def score_threshold(window, cutoff):
    """
    window  : array of smoothed errors
    cutoff  : one candidate threshold
    returns : the score of that candidate (higher is better)
    """
    # make a True/False array: which values are above the cutoff
    isItAbove = []
    count_true_isItAbove = 0
    below = []
    for i in range(0, len(window)):
        if (window[i] > cutoff):
            isItAbove.append(True)
            count_true_isItAbove +=1
        else:
            isItAbove.append(False)
            # get the values below the cutoff
            below.append(window[i])
    if (count_true_isItAbove == 0 or len(below) < 2):
        return 0

    # compute delta_mean and delta_std
    delta_mean = statistics.mean(window) - statistics.mean(below)
    delta_std = statistics.stdev(window) - statistics.stdev(below)

    # count num_above and num_sequences
    num_above = count_true_isItAbove
    num_sequence = count_sequences(isItAbove)
    # compute and return the score from the formula at the top
    score =  (delta_mean/ statistics.mean(window) + delta_std / statistics.stdev(window)) / (num_above + num_sequence ** 2)
    return score


def best_threshold(window, z_values):
    """
    returns : the candidate cutoff with the highest score
    """
    # get the candidates
    candidates = candidate_thresholds(window, z_values)
    # score each one
    scores = []
    # keeps track which is the highest score
    max_index = 0
    for i in range(0, len(candidates)):
        scores.append(score_threshold(window, candidates[i]))
        if(scores[i] > scores[max_index]):
            max_index = i
    # return the candidate with the highest score (argmax)
    return candidates[max_index]



if __name__ == "__main__":
    # Check by hand with the window [1, 1, 1, 2, 1, 9, 10]:
    # a cutoff of 5 should score higher than a cutoff of 1.5
    # call score_threshold for both cutoffs and print the two scores
    window = np.array([1, 1, 1, 2, 1, 9, 10], dtype=float)
    print("cutoff 5  :", score_threshold(window, 5))
    print("cutoff 1.5:", score_threshold(window, 1.5))
