import numpy as np
import os

folder = os.path.dirname(os.path.abspath(__file__))

train = np.load(os.path.join(folder, "MSL_train.npy"))
test = np.load(os.path.join(folder, "MSL_test.npy"))
labels = np.load(os.path.join(folder, "MSL_test_label.npy"))

print("Train shape:", train.shape)
print("Test shape:", test.shape)
print("Labels shape:", labels.shape)
print("Unique labels:", np.unique(labels))
# Select Feature 1
first_feature = train[:, 0]

print("Feature 1 shape:", first_feature.shape)
print("Minimum:", first_feature.min())
print("Maximum:", first_feature.max())
print("Unique values:", np.unique(first_feature).size)
print("98th percentile:", np.quantile(first_feature, 0.98))
