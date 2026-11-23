"""
import/ open and read from auto encoder socres and apply hundmand/NDT method on it
"""
import numpy as np
import os
import sys
folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(folder))
from ndt import run_ndt, flags_from_sequences


# open auto encoder
path = os.path.join(folder, "autoencoder_scores.npz")
z = np.load(path, allow_pickle=True)

# read score_test named scores, y_test named labels, and ts_test named times

#score_test: the anomaly score of each window.
#   Higher means more suspicious. It is the reconstruction
#   error of an autoencoder trained only on normal data.
#   It is in raw units with no upper bound (roughly 0.01 to 10).

#y_test: the true label of each window. 1 = attack, 0 = normal.
#   About 12.25% of windows are attacks.

#ts_test: the timestamp of each window, one every 10 seconds,
#   from 2015-12-28 10:29:13 to 2016-01-02 14:59:54.
#   A window is 5 steps (50 seconds) long and takes the label of its last step.

scores = z["score_test"]
labels = z["y_test"]
times  = z["ts_test"]

# convert 0 and 1 labels to booleans
labels = labels.astype(bool)

# print ercentiles of scores
percentile  = np.percentile(scores, [50, 90, 95, 99, 99.9])

print(percentile)
#Print the average score of
# the normal windows and of the attack windows
avg_score_attack=  np.mean(scores[labels])
avg_score_normal= np.mean(scores[~ labels])
print(f"avg normal scores: {avg_score_normal} avg attack scores: {avg_score_attack}")
num_of_attacks =  labels.sum()
print(f"number of attacks {num_of_attacks}")

# run ndt on the it
alpha = 0.5
z_values = [1, 2, 3, 4, 5]
window_size = 500
step = 500
p = 0.1

results = run_ndt(scores, alpha, z_values, window_size, step, p)
flags = flags_from_sequences(results, len(scores))

print(f"{len(results)} is the number of sequences found.")
print(f"{flags.sum()} is how many windows were flagged.")
print(f"{flags.mean()} is the share flagged.")
