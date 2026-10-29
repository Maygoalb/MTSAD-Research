import numpy as np
import os
import sys

# Find the parent folder (siffer)
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_folder)

from spot import SPOT

folder = os.path.dirname(os.path.abspath(__file__))

# Load SMD data
train = np.load(os.path.join(folder, "SMD_train.npy"))
test = np.load(os.path.join(folder, "SMD_test.npy"))
labels = np.load(os.path.join(folder, "SMD_test_label.npy"))

# Select Feature 1
train = train[:, 0]
test = test[:, 0]
labels = labels.astype(bool)

# Train SPOT
spot = SPOT(q=0.005, level=0.98)
spot.fit(train)

# Detect anomalies
flags, thresholds = spot.run(test)

# Evaluate
TP = np.sum(flags & labels)
FP = np.sum(flags & ~labels)
FN = np.sum(~flags & labels)
TN = np.sum(~flags & ~labels)

precision = TP / (TP + FP) if TP + FP else 0
recall = TP / (TP + FN) if TP + FN else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
accuracy = (TP + TN) / len(labels)

print("\nSMD Results - Feature 1")
print("Detected anomalies:", flags.sum())
print("TP:", TP, "FP:", FP, "FN:", FN, "TN:", TN)
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-score: {f1:.3f}")
print(f"Accuracy: {accuracy:.3f}")
