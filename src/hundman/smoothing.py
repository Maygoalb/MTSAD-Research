"""

Formula:
    s_t = alpha * e_t + (1 - alpha) * s_(t-1)
    s_0 = e_0
"""
import numpy as np

# Exponentially Weighted Moving Average
def ewma(error, alpha):
    """
    errors : list or array of raw errors, one per time step
    alpha  : weight on the newest error, between 0 and 1
    returns: array of smoothed errors, same length as errors
    """
    # convert errors to a NumPy array of floats
    error_arr = np.array(error, dtype=float)

    # make an empty array "smoothed" with the same length as errors
    smoothed = np.zeros(len(error_arr))

    # set the first smoothed value equal to the first error
    smoothed[0] = error_arr[0]

    # loop from the second item to the end
    # smoothed[i] = alpha * errors[i] + (1 - alpha) * smoothed[i - 1]
    for i in range(1, len(smoothed)):
        smoothed[i] = alpha * error_arr[i] + (1- alpha) * smoothed[i-1]

    # return smoothed
    return smoothed


if __name__ == "__main__":
    # Check by hand: [1, 1, 1, 10, 1] with alpha = 0.5
    # should give   [1, 1, 1, 5.5, 3.25]
    # What EWMA does:
    # it replaces each raw error with a
    # blend of the new error and the previous
    # smoothed value. A single spike gets softened,
    # and its effect fades over the next few steps.
    # the raw error jumps to 10, but the
    # smoothed value only rises to 5.5.
    # Half of it comes from the old, calm history.
    result = ewma([1, 1, 1, 10, 1], 0.5)
    print(result)
