#!/usr/bin/env python
"""Basic raytracer to create simple images """
from engine import RenderEngine
from scene import Scene
import argparse
import importlib
import os
from multiprocessing import  cpu_count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Path to scene file (without extension .py)")
    parser.add_argument("-p", "--processes",action='store', 
                        type=int, dest='processes', default=0,
                        help="Number of processes (0=auto)",
                        )
    args = parser.parse_args()
    if args.processes == 0:
        process_count = cpu_count()
    else:
        process_count = args.processes
    print(f"Process count = {process_count}")
    mod = importlib.import_module(args.scene)
    
    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine()
    
    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    with open(mod.RENDERED_IMG, 'w') as img_fileobj:
        engine.render_multiprocess(scene, process_count, img_fileobj, mod.SAMPLES_PER_PIXEL)


if __name__ == '__main__':
    main()