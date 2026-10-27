# import numpy as np
# import os

# def load_smd_data(folder_name, machine="machine-1-1"):
#     folder = os.path.dirname(os.path.abspath(__file__))

#     path = os.path.join(
#         folder, "SMD", folder_name, machine + ".txt"
#     )

#     data = np.loadtxt(path, delimiter=",")

#     print(f"Loaded {machine} from {folder_name}")
#     print(f"Shape: {data.shape}")

#     # Select the first feature
#     if data.ndim > 1:
#         return data[:, 0]

#     return data

import numpy as np
import os

folder = os.path.dirname(os.path.abspath(__file__))

path = os.path.join(folder, "SMD", "SMD_train.npy")

data = np.load(path)
first_feature = data[:, 0]

test_data = np.load(os.path.join(folder, "SMD", "SMD_test.npy"))
labels = np.load(os.path.join(folder, "SMD", "SMD_test_label.npy"))

# Select Feature 1
test_feature = test_data[:, 0]

print("Test shape:", test_data.shape)
print("Feature 1 shape:", test_feature.shape)
print("Labels shape:", labels.shape)
print("Unique labels:", np.unique(labels))
