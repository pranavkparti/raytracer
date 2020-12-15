#from image import Image
from vector import Vector, Point, Color
from sphere import Sphere
from engine import RenderEngine
from light import Light
from material import Material, ChequeredMaterial
from camera import Camera

#image dimensions
WIDTH = 960
HEIGHT = 540
ASPECT_RATIO = WIDTH / HEIGHT
#camera attributes
VIEWPORT_HEIGHT = 2.0

RENDERED_IMG = 'images/2balls.ppm'
#CAMERA = Vector(0, -0.35, -1)
CAMERA  = Camera(VIEWPORT_HEIGHT , ASPECT_RATIO)
# OBJECTS = [
#     #ground plane
#     Sphere(Point(0,10000.5,1), 10000, ChequeredMaterial(
#                                         color1=Color.from_hex("#420500"), 
#                                         color2=Color.from_hex("#e6b87d"),
#                                         ambient=0.2,
#                                         reflection=0.2,
#                                         )
#                                     ),
#     #blue ball
#     Sphere(Point(0.75,-0.1,1), 0.6, Material(Color.from_hex('#0000ff'))),
#     #pink ball
#     Sphere(Point(-0.75,-0.1,2.25), 0.6, Material(Color.from_hex('#803980'))),
#     ]

OBJECTS = [Sphere(Point(0,0,-1), 0.5, Material(Color.from_hex('#00ff00'))),
            Sphere(Point(0,100.5,-1), 100, Material(Color.from_hex('#00ff00')))]
LIGHTS = [
    Light(Point(1.5, -0.5, -10.0), Color.from_hex("#ffffff")),
    Light(Point(-0.5, -10.5, 0), Color.from_hex("#e6e6e6")),
    ]
