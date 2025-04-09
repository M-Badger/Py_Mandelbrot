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

from PIL import Image
import time
from matplotlib.colors import LinearSegmentedColormap

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def get_new_colormap():
    # Define the colors and their positions using RGB values
    colors = [
        (0.0, (0.0, 0.0, 0.0)),  # Black
        (0.1, (1.0, 0.0, 0.0)),  # Red
        (0.3, (1.0, 1.0, 0.0)),  # Yellow
        (1.0, (1.0, 1.0, 1.0))   # White
    ]
    # Create the colormap
    return LinearSegmentedColormap.from_list("CustomColormap", colors)

# Define the range for the real and imaginary parts of c; the full set is contained in the range (-2.0, -1.2i) to (0.5, 1.2i)
real_min, real_max = -0.777120669579820285689, -0.777120217041497188109
imag_min, imag_max = 0.126857111509958518549, 0.126857366062765260939

# Algorithm
iteration_limit = 5000 # The higher the max iterations, the greater the precision but the longer it will take

# Image
width = 1000
height = int(width * (abs(imag_max - imag_min) / (real_max - real_min))) # Image height is scaled such that the width/height ratio matches the real and imaginary ranges set in the variables above
image = Image.new('RGB', (width, height)) # Create image in 'RGB' mode
pixels = image.load()

# Use a colormap from matplotlib, such as 'binary', 'rainbow', 'viridis', 'plasma', 'inferno', etc. For a full list, see https://matplotlib.org/stable/users/explain/colors/colormaps.html
# colormap = cm.colormaps['YlOrRd']

# Or create a new colormap
colormap = get_new_colormap()

# Start the timer
start_time = time.time()

for x in range(width):
    for y in range(height):
        # Map pixel coordinates to the complex plane
        real = real_min + (x / width) * (real_max - real_min)
        imag = imag_min + (y / height) * (imag_max - imag_min)
        c = complex(real, imag)
        m = mandelbrot(c, iteration_limit)
        if m == iteration_limit:
            # Pixels inside the set are black
            pixels[x, y] = (0, 0, 0)
        else:
            # Normalize the iteration count to [0, 1] for colormap
            normalised = m / iteration_limit
            # Get RGB values from the colormap
            r, g, b, _ = colormap(normalised)
            # Convert to 8-bit integers
            pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")

# Transpose the image vertically because it is created from bottom left to top right ((real_min, imag_min) to (real_max, imag_max)) but applied to the image canvas top left to bottom right
image = image.transpose(method = Image.Transpose.FLIP_TOP_BOTTOM)
image.save('mandelbrot.png')
image.show()