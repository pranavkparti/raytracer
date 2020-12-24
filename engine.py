import math
from random import random, uniform
from hittable import Hit_Record
from image import Image
from ray import Ray
from vector import Point, Color
from sphere import Sphere
from material import Material
import tempfile
from pathlib import Path
import shutil
from multiprocessing import Value, Process
from camera import Camera
from vector import Vector
from sphere import Sphere

class RenderEngine:
    """Renders 2D objects into 3D objectys using ray tracing"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001
    INFINITY = float('inf')
    PI = math.pi

    def degrees_to_radians(self, degrees):
        return degrees * self.PI / 180.0
    
    # def clamp(self, x, min, max):
    #     if x > max:
    #         return max
    #     elif x <min:
    #         return min
    #     else:
    #         return x

    def render_multiprocess(self, scene, process_count, img_fileobj, samples_per_pixel):
        def split_range(count, parts):
            d, r = divmod(count, parts)
            return [
                (i*d + min(i, r), (i+1)*d + min(i+1, r)) for i in range(parts)
            ]
        #locally declared for speed and ease of access   
        width = scene.width
        height = scene.height
        ranges = split_range(height, process_count)
        temp_dir = Path(tempfile.mkdtemp())
        tmp_file_tmpl = 'raytracer-part-{}.temp'
        processes = []
        try:
            rows_done = Value('i', 0)
            for hmin, hmax in ranges:
                part_file = temp_dir / tmp_file_tmpl.format(hmin)
                processes.append(Process(
                    target=self.render, 
                    args=(scene, hmin, hmax, part_file, rows_done, samples_per_pixel),
                    )
                )
            #start all the processes
            for process in processes:
                process.start()
            #wait for all processes to finish
            for process in processes:
                process.join()
            #construct image by joining all the parts
            Image.write_ppm_header(img_fileobj, height=height, width=width)
            for hmin, _ in ranges:
                part_file = temp_dir / tmp_file_tmpl.format(hmin)
                img_fileobj.write(open(part_file, 'r').read())
        finally:
            shutil.rmtree(temp_dir)

    def render(self, scene, hmin, hmax, part_file, rows_done, samples_per_pixel):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height
        x0 = -1.0
        x1 = +1.0
        xstep = (x1 - x0) / (width - 1) #delta
        y0 = -(1.0 / aspect_ratio)
        y1 = +(1.0 / aspect_ratio)
        ystep = (y1 - y0) / (height - 1)

        camera = scene.camera
        pixels = Image(width, hmax - hmin)

        #defining ray_color
        def ray_color(ray, scene, depth):
            color = Color(0, 0, 0)
            if depth <= 0:
                return Color(0, 0, 0)
                #return Color(0, 0, 0)
            #objs = scene.objects
            #0.001 to solve shadow acne problem
            dist_min, rec = self.find_nearest(ray, 0.001, self.INFINITY, scene)
            zero = Color()

            #rec = obj_hit.intersects(ray, 0, self.INFINITY)
            #t = Sphere(Point(0,0,-1), 0.5, Material(Color.from_hex('#00ff00'))).intersects(ray,-1,10)
            if rec is not None:
                t = rec.t
            else:
                t = None
            if t is not None:
                #color += self.color_at(rec)
                scatter_info = rec.material.scatter(ray, rec)
                if scatter_info :
                    return ray_color(scatter_info.scattered, scene, depth - 1).indimul(scatter_info.attenuation) 
                else:
                    return zero
                # target = rec.point + rec.normal + Sphere.random_unit_vector()
                # return 0.5 * ray_color(Ray(rec.point, target - rec.point), scene, depth - 1)
            
            unit_direction = ray.direction
            t = 0.5 * (unit_direction.y + 1.0)
            return (t) * Color(1, 1, 1) + (1 - t) * Color(0.5, 0.7, 1.0)

        for j in range(hmin, hmax):
            for i in range(width):
                pixel_color = Color(0, 0, 0)
                for _ in range(samples_per_pixel):
                    u = (i + random()) / (width - 1)
                    v = (j + random()) / (height - 1)
                    #ray = Ray(camera.origin, camera.lower_left_corner + u * camera.horizontal + v * camera.vertical - camera.origin)
                    ray = camera.get_ray(u, v)
                    pixel_color += ray_color(ray, scene, self.MAX_DEPTH)
                pixels.set_pixel(i, j - hmin, pixel_color)
        
            if rows_done:
                with rows_done.get_lock():
                    rows_done.value += 1
                    print("{:3.0f}%".format(float(rows_done.value) / float(height) * 100), end='\r')

        with open(part_file, 'w') as part_fileobj:
            pixels.write_ppm_raw(part_fileobj, samples_per_pixel)


    def find_nearest(self, ray, tmin, tmax, scene):
        closest_so_far = tmax
        obj_hit = None 
        # rec = Hit_Record()
        for obj in scene.objects:
            rec = obj.intersects(ray, tmin, tmax)
            if rec is not None:
                dist = rec.t
            else:
                dist = None
            if dist is not None and (obj_hit is None or dist < closest_so_far):
                closest_so_far = dist
                obj_hit = rec
        return (closest_so_far, obj_hit)

    def color_at(self, rec):
        pass