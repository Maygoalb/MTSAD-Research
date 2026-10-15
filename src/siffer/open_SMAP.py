import numpy as np
import os
def load_smap_data(filename):
    # Use the full, absolute path that the script discovered
    folder = os.path.dirname(os.path.abspath(__file__))
    arr = np.load(os.path.join(folder, filename))

    # Now you can inspect your dataset!
    print(f"Data loaded perfectly! {filename} Shape: {arr.shape}")
    # This grabs all rows, but only the first column
    if arr.ndim > 1:
        first_col = arr[:, 0]
    else:
        # if array is 1d
        first_col = arr
    return first_col

    # print("\n --- First Column Data --- ")
    # print(first_col)
