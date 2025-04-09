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

def mandelbrot(c, max_iter):
    z = 0
    for iterations in range(max_iter):
        if abs(z) > 2:
            return iterations
        z = z*z + c
    return max_iter

# Image
width, height = 1000, 1000 # The width/height ratio matches the range of the real and imaginary ranges set in the for loops below, for c: real part from -2 to 2, imaginary part from -2 to 2
image = Image.new('RGB', (width, height)) # Create image in 'RGB' mode
pixels = image.load()

# Start the timer
start_time = time.time()

for x in range(width):
    for y in range(height):
        c = complex(-2 + (x / width) * 4, -2 + (y / height) * 4)
        m = mandelbrot(c, 256)
        color = 255 - int(m * 255 / 256)
        pixels[x, y] = (color, color, color)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")

# Transpose the image vertically because it is created from bottom left to top right ((-2,-2) to (2,2)) but applied to the image canvas top left to bottom right
image = image.transpose(method = Image.Transpose.FLIP_TOP_BOTTOM)
image.save('mandelbrot.png')
image.show()