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

def mandelbrot(c, max_iter):
    z = 0
    for iterations in range(max_iter):
        if abs(z) > 2:
            # Return the normalised escape value
            return iterations - np.log(np.log(abs(z))) / np.log(2)
        z = z*z + c
    return max_iter

# Algorithm
iteration_limit = 30 # The higher the max iterations, the less banding will be visible but the more it will look like a 2-colour plot

# Image
width, height = 1000, 960 # The width/height ratio matches the range of the real and imaginary ranges set in the for loops below, for c: real part from -2 to 0.5, imaginary part from -1.2 to 1.2
image = Image.new('L', (width, height)) # Create image in 'L' mode for greyscale (L = luminance)
pixels = image.load()

# Start the timer
start_time = time.time()

for x in range(width):
    for y in range(height):
        real = -2 + (x / width) * 2.5  # Real part: -2 to 0.5
        imag = -1.2 + (y / height) * 2.4  # Imaginary part: -1.2 to 1.2
        c = complex(real, imag)
        m = mandelbrot(c, 256)
        # Normalize the value to [0, 255] for grayscale luminance
        grayscale = int(255 * (m / iteration_limit))
        pixels[x, y] = grayscale

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")

# Transpose the image vertically because it is created from bottom left to top right ((-2, -1.2) to (0.5, 1.2)) but applied to the image canvas top left to bottom right
image = image.transpose(method = Image.Transpose.FLIP_TOP_BOTTOM)
image.save('mandelbrot.png')
image.show()