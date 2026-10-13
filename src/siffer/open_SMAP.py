import numpy as np

# Use the full, absolute path that the script discovered
data = np.load(r'c:\Users\msb06\Desktop\MTSAD REPO\MTSAD-Research\src\siffer\SMAP_train.npy')

# Now you can inspect your dataset!
print(f"Data loaded perfectly! Shape: {data.shape}")
# This shows the first few rows/columns and last few rows/columns
# This grabs rows 0 to 4, and shows all 25 columns for them
# [:, 0] means "give me every row, but only the 0-th column"
print("\n--- First Column Data (First 10 values) ---")
print(data[:10, 0])
