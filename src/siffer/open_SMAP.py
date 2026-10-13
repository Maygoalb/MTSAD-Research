import numpy as np
def load_smap_data():
    # Use the full, absolute path that the script discovered
    arr = np.load(r'c:\Users\msb06\Desktop\MTSAD REPO\MTSAD-Research\src\siffer\SMAP_train.npy')

    # Now you can inspect your dataset!
    print(f"Data loaded perfectly! Shape: {arr.shape}")
    # This grabs all rows, but only the first column
    first_col = arr[:, 0]

    print("\n --- First Column Data --- ")
    print(first_col)
    return first_col
