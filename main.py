#!/usr/bin/env python
"""Basic raytracer to create simple images """
from image import Image
from color import Color
from vector import Vector
from point import Point
from sphere import Sphere
from scene import Scene
from engine import RenderEngine
from light import Light
from material import Material
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("imageout", help="Path to rendered image")
    args = parser.parse_args()
    WIDTH = 320
    HEIGHT = 200
    camera = Vector(0, 0, -1)
    objects = [Sphere(Point(0,0,0), 0.5, Material(Color.from_hex('#ff0000')))]
    lights = [Light(Point(1.5, -0.5, -10.0), Color.from_hex("#ffffff"))]
    scene = Scene(camera, objects, lights, WIDTH, HEIGHT)
    engine = RenderEngine()
    image = engine.render(scene)

    with open(args.imageout, 'w') as img_file:
        image.write_ppm(img_file)

#make traffic lights
def make_traffic():
    WIDTH = 320
    HEIGHT = 200
    camera = Vector(0, 0, -1)
    objects = [
        Sphere(Point(0,-0.75,1), 0.25, Color.from_hex('#ff0000')),
        Sphere(Point(0,0,1), 0.25, Color.from_hex('#00ff00')),
        Sphere(Point(0,0.75,1), 0.25, Color.from_hex('#0000ff'))
        ]
    scene = Scene(camera, objects, WIDTH, HEIGHT)
    engine = RenderEngine()
    image = engine.render(scene)

    with open('images/make_traffic.ppm', 'w') as img_file:
        image.write_ppm(img_file)

#make_traffic()

#make test ppm
def make_test():
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

    with open('images/make_test.ppm', 'w') as img_file:
        im.write_ppm(img_file)

#make_test()

#make gradient
def make_gradient():
    WIDTH = 255
    HEIGHT = 255
    red = Color(x=1.0, y=0.0, z=0.0)
    pix = Image(WIDTH, HEIGHT)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            pix.set_pixel(x, y, red*y/255)
    with open('images/make_gradient.ppm', 'w') as img_file:
        pix.write_ppm(img_file)

#make_gradient()


if __name__ == '__main__':
    main()