#!/usr/bin/env python
"""Basic raytracer to create simple images """
from image import Image
from color import Color

def main():
    WIDTH = 3
    HEIGHT = 2
    im = Image(WIDTH, HEIGHT)
    red = Color(x=1, y=0, z=0)
    green = Color(x=0, y=1, z=0)
    blue = Color(x=0, y=0, z=1) 
    
    im.set_pixel(0, 0, red)
    im.set_pixel(1, 0, green)
    im.set_pixel(2, 0, red)
    
    im.set_pixel(0, 1, red + green)
    im.set_pixel(1, 1, red + blue + green)
    im.set_pixel(2, 1, red * 0.001)

    with open('images/test.ppm', 'w') as img_file:
        im.write_ppm(img_file)

if __name__ == '__main__':
    main()