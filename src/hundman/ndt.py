"""
This file does not do new math. It calls the pieces you already wrote:
    smoothing.py : ewma
    threshold.py : best_threshold
    sequences.py : find_sequences, severity_score
    pruning.py   : prune

Pipeline for one run:
    raw errors -> smooth -> split into windows -> for each window:
        best threshold -> find sequences -> prune -> score
    -> combine the results from all windows
"""
import numpy as np

from smoothing import ewma
from threshold import best_threshold
from sequences import find_sequences, severity_score
from pruning import prune


def detect_in_window(window, z_values, p):
    """
    window   : array of smoothed errors (one window)
    z_values : list of z multipliers to try
    p        : minimum percent drop for pruning
    returns  : list of (start, end, score), positions LOCAL to this window
    """
    # get the best threshold for this window (best_threshold)
    best_th = best_threshold(window, z_values)
    # find the sequences above that threshold (find_sequences)
    above_th =  find_sequences(window,best_th)
    # prune them (prune)
    seq_left = prune(window, above_th, p)
    # for each sequence that is left, compute its severity (severity_score)
    results = []
    for s in seq_left:
        score = severity_score(window,s, best_th)
        results.append((s[0], s[1], score))
    # return a list of (start, end, score)
    return results

def run_ndt(errors, alpha, z_values, window_size, step, p):
    """
    errors      : array of raw prediction errors, one per time step
    alpha       : EWMA smoothing weight
    z_values    : list of z multipliers to try
    window_size : how many smoothed errors in one window
    step        : how far the window moves each time
    p           : minimum percent drop for pruning
    returns     : list of (start, end, score), positions GLOBAL (whole error array)
    """
    #  smooth the errors
    smoothed =  ewma(errors, alpha)
    #  make an empty list for the results
    results = []
    #  loop over the start position of each window:
    #       start = 0, step, 2 * step, ... while the window still fits
    for i in range(0, len(smoothed) - window_size + 1, step):
        #  cut out the window: smoothed[start : start + window_size]
        w = smoothed[i : i +window_size]
        #  call detect_in_window on it
        r = detect_in_window(w, z_values, p)
        #  shift each (start, end, score) by the window's start position,
        #  so the positions match the whole error array
        for (s, e, score) in r:
             #  add them to the results list
            results.append((s + i, e + i, score))
    # DECISION: what happens to the last, shorter piece of data at the end?
    #           (skip it, or use a shorter last window?)
    # DECISION: if step < window_size the windows overlap and the same sequence
    #           can be found twice. Simplest start: step = window_size.
    # the last partial window is skipped.

    # return the results
    return results


def flags_from_sequences(results, length):
    """
    results : list of (start, end, score)
    length  : length of the error array
    returns : array of True/False, True for every position inside a sequence
    """
    # make an array of False with the given length
    array = []
    for i in range(0, length):
        array.append(False)
    # for each (start, end, score), set those positions to True (end included)
    for r in results:
        for i in range(r[0], r[1]+1):
            array[i] = True

    # return it (this is what metrics.py will compare with the labels)
    return np.array(array)


if __name__ == "__main__":
    # Check on made-up errors: mostly small, with one clear burst
    errors = np.array([1, 1, 1, 2, 1, 1, 1, 1, 9, 10, 9, 1, 1, 1, 1, 1], dtype=float)
    z_values=[2, 3, 4, 5]
    # call run_ndt with, for example, alpha=0.5, z_values=[2, 3, 4, 5],
    #  window_size=16, step=16, p=0.1 and print the result
    r = run_ndt(errors, 0.5, z_values,16, 16, 0.1 )
    print(f"run ndt:{r}")
    # Expected: one sequence somewhere around positions 8 to 10
