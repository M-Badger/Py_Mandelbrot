# Badger Py Mandelbrot
Simple Python program that draws the Mandelbrot set
This project was undertaken to learn Python syntax and basic Python skills

## Python Version
The project was written using Python version 3.13

## Requirements
- pillow
- numpy
- matplotlib
- gmpy2

## Versions
### v0.1 Black and White
Draws a very simple Mandelbrot image with white assigned to pixels in the set and black assigned to pixels outside the set

### v0.2 Greyscale
Draws a simple Mandelbrot image where pixels outside the set are different shades of grey depending on the number of iterations required to confirm the point is outside the set

### v0.3 Colourmap
Draws a simple colourised version of the Mandelbrot set using a colour map. Colour maps from *matplotlib* are used ('colormap' class)

### v0.4 Scaled Colourmap
The width of the created image is scaled based on the complex points provided and the height of the image such that the ratios match

### v0.5 Optimised
Two optimisations are introduced in order to i;prove calculation performance
1. Multitasking using 'ProcessPoolExecutor' from 'concurrent.futures'
2. Caching the translation of iteration results into colours to avoid identical repeat calls to matplotlib interpolation code

### v 1.0 Precision
The Mandelbrot algorithm uses the Python 'Decimal' class in place of the 'float' class to improve floating point calculation precision
**Calculation times are significantly increased**

### gmpy2 branch
**DO NOT USE**
The Mandelbrot algorithm is modified to use the *gmpy2* library (optimized, C-coded Python extension module that supports fast multiple-precision arithmetic). On this developers equipment the code crashed Windows consistently (quite possibly due to my limited competence)

## License
Copyright (C) 2025  Mike Conroy
The author hereby disclaims all copyright interest in the program “Badger Py Mandelbrot”

This program is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <https://www.gnu.org/licenses/>.