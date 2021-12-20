import numpy as np
from scipy.ndimage import convolve

# Load data
with open('/home/swann/adventofcode/2021/inputs/day_20.txt') as f:
    lines = [l.strip() for l in f.readlines()]

algo = tuple([1 if c == '#' else 0 for c in lines[0]])
img_arr = np.array([[1 if c=='#' else 0 for c in l] for l in lines[2:]])

# Create the vectorized decode function
decode_vec = np.vectorize(lambda x: algo[x])

# Create a convolution filter that maps bit values to each pixel
filter = np.array([
    [256, 128, 64],
    [32, 16, 8],
    [4, 2, 1]
])[::-1, ::-1]

# Padding the array to max expected size
img_filtered = np.pad(img_arr, 50)

# Iterating: convolving + decoding
for i in range(1, 51):
    img_filtered = decode_vec(convolve(img_filtered, filter))
    if i in [2, 50]:
        print(f'iter {i:02,}; lit pixels: {img_filtered.sum().sum():6,} secs')
