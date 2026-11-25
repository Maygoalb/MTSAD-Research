"""
import/ open and read from auto encoder socres and apply hundmand/NDT method on it
"""
import numpy as np
import os
import sys
folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(folder))
from ndt import run_ndt, flags_from_sequences
from metrics import confusion_counts, precision_recall_f1


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

print(f"{len(results)} is the number of sequences found.A run of points in a row that are above the threshold.")
print(f"{flags.sum()} is how points were flagged. Flagged points Count every point inside the sequences.")
print(f"{flags.mean()} is the share flagged.")


# calculate F1 scores
TP, FP, FN, TN = confusion_counts(flags, labels)
precision, recall, f1 = precision_recall_f1(TP, FP, FN)

print(f"TP={TP} FP={FP} FN={FN} TN={TN}")
print(f"precision={precision:.3f} recall={recall:.3f} f1={f1:.3f}")

false_alarms = flags & ~labels     # flagged, but normal
missed = ~flags & labels           # real attack, not flagged
#print how many there are.
print("false alarms:", false_alarms.sum())
print("missed attacks:", missed.sum())
# print the average score of each group.
print("avg score of false alarms:", np.mean(scores[false_alarms]))
print("avg score of missed attacks:", np.mean(scores[missed]))
