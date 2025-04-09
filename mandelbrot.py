#  ========================================================================
#  Badger Py Mandelbrot
#  Copyright (C) 2025  Mike Conroy
#
#  The author hereby disclaims all copyright interest in the program “Badger Py Mandelbrot”
#
#  This program is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software Foundation, 
#  either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.
#  ========================================================================

import numpy as np
import time
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap
from concurrent.futures import ProcessPoolExecutor

# The core mandelbrot iterative loop to determine if a point is inside or outised the set
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# Together with the ProcessPoolExecutor code below this function allows for parallelisation
def compute_row(y):
    row = []
    imag = imag_min + (y / height) * imag_range
    for x in range(width):
        real = real_min + (x / width) * real_range
        c = complex(real, imag)
        m = mandelbrot(c, iteration_limit)
        if m == iteration_limit:
            # Pixels inside the set are black
            row.append((0, 0, 0))
        else:
            # Normalise the iteration count to [0, 1] for colormap
            normalised = m / iteration_limit
            # Get RGB values from the colormap
            r, g, b = get_colour(normalised)
            row.append((r, g, b))
    return y, row

# Creates a colormap from matplotlib
def get_new_colourmap():
    # Define the colours and their positions (from 0 to 1) using RGB values
    colours = [
        (0.0, (0.0, 0.0, 0.0)),  # Black
        (0.1, (1.0, 0.0, 0.0)),  # Red
        (0.3, (1.0, 1.0, 0.0)),  # Yellow
        (1.0, (1.0, 1.0, 1.0))   # White
    ]
    # Create the colormap
    return LinearSegmentedColormap.from_list("CustomColormap", colours)

# Optimises the translation of iteration results into colours by using a cache to avoid identical repeat calls to matplotlib interpolation code
def get_colour(normalised):
    if normalised not in colourmap_cache:
        r, g, b, _ = colourmap(float(normalised))
        colourmap_cache[normalised] = (int(r * 255), int(g * 255), int(b * 255))
    return colourmap_cache[normalised]

# Define the range for the real and imaginary parts of c; the full set is contained in the range (-2.0, -1.2i) to (0.5, 1.2i)
real_min, real_max = -0.777120669579820285689, -0.777120217041497188109
imag_min, imag_max = 0.126857111509958518549, 0.126857366062765260939

# Algorithm
iteration_limit = 5000 # The higher the max iterations, the greater the precision but the longer it will take

# Image
width = 1000
height = int(width * (abs(imag_max - imag_min) / (real_max - real_min))) # Image height is scaled such that the width/height ratio matches the real and imaginary ranges set in the variables above

# Create a new colormap or Use a colormap from matplotlib, such as 'binary', 'rainbow', 'viridis', 'plasma', 'inferno', etc. For a full list, see https://matplotlib.org/stable/users/explain/colors/colormaps.html
# colourmap = cm.colormaps['YlOrRd']
colourmap = get_new_colourmap()

# Use a colormap cache to speed the determination of the pixel colour
colourmap_cache = {}

# Precalculate for loop constant values
real_range = real_max - real_min
imag_range = imag_max - imag_min

# Together with the compute_row function above this code allows for parallelisation
if __name__ == "__main__":

    # Start the timer
    start_time = time.time()

    # Initialise the image array
    image_array = np.zeros((height, width, 3), dtype=np.uint8)

    # Use ProcessPoolExecutor to compute rows in parallel
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_row, range(height)))
    
    # Process the results and update the image array
    for y, row in results:
        for x, colour in enumerate(row):
            image_array[y, x] = colour

    # Create the image from the array
    image = Image.fromarray(image_array, 'RGB')

    # Transpose the image vertically because it is created from bottom left to top right ((real_min, imag_min) to (real_max, imag_max)) but applied to the image canvas top left to bottom right
    image = image.transpose(method = Image.Transpose.FLIP_TOP_BOTTOM)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")

    # Save and display the image
    image.save('mandelbrot.png')
    image.show()