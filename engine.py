import math
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

class RenderEngine:
    """Renders 2D objects into 3D objectys using ray tracing"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001
    INFINITY = float('inf')
    PI = math.pi

    def degrees_to_radians(self, degrees):
        return degrees * self.PI / 180.0

    def render_multiprocess(self, scene, process_count, img_fileobj):
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
                    args=(scene, hmin, hmax, part_file, rows_done),
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

    def render(self, scene, hmin, hmax, part_file, rows_done):
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
        def ray_color(ray, scene):
            #objs = scene.objects
            dist_min, rec = self.find_nearest(ray, 0, self.INFINITY, scene)
            #rec = obj_hit.intersects(ray, 0, self.INFINITY)
            #t = Sphere(Point(0,0,-1), 0.5, Material(Color.from_hex('#00ff00'))).intersects(ray,-1,10)
            if rec is not None:
                t = rec.t
            else:
                t = None
            if t is not None:
                #N = (ray.at(rec.t) - Point(0,0,-1)).normalize()
                #return 0.5 * Color(N.x + 1, N.y + 1, N.z + 1)
                return 0.5 * (rec.normal + Color(1,1,1))
            unit_direction = ray.direction
            t = 0.5 * (unit_direction.y + 1.0)
            return (1 - t) * Color(1, 1, 1) + (t) * Color(0.5, 0.7, 1.0)

        for j in range(hmin, hmax):
            for i in range(width):
                u = i / (width - 1)
                v = j / (height - 1)
                ray = Ray(camera.origin, camera.lower_left_corner + u * camera.horizontal + v * camera.vertical - camera.origin)
                pixel_color = ray_color(ray, scene)
                pixels.set_pixel(i, j - hmin, pixel_color)
        
            if rows_done:
                with rows_done.get_lock():
                    rows_done.value += 1
                    print("{:3.0f}%".format(float(rows_done.value) / float(height) * 100), end='\r')

        with open(part_file, 'w') as part_fileobj:
            pixels.write_ppm_raw(part_fileobj)

    def ray_trace(self, ray, scene, depth=0):
        color = Color(0,0,0)
        #find nearest object to ray in the scene
        dist_hit, object_hit = self.find_nearest(ray, scene)
        if object_hit is None:
            return color
        hit_pos = ray.origin + ray.direction * dist_hit
        #hit_pos = Ray(ray.origin, ray.direction).at(dist_hit)
        hit_normal = object_hit.normal(hit_pos)
        color += self.color_at(object_hit, hit_pos, hit_normal, scene)
        if depth < self.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = ray.direction - 2* ray.direction.dot_product(hit_normal) * hit_normal
            new_ray = Ray(new_ray_pos, new_ray_dir)
            #Attenuate reflected ray by reflection coefficient
            #bouncing around causes the ray to lose energy
            color += self.ray_trace(new_ray, scene, depth+1) * object_hit.material.reflection 
        return color

    # def find_nearest(self, ray, scene):
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

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

    def color_at(self, obj_hit, hit_pos, normal, scene):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera - hit_pos
        specular_k = 50
        #ambient color
        color = material.ambient * Color.from_hex("#ffffff")
        #light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            #diffuse shading (lambert)
            color += obj_color * material.diffuse * max(normal.dot_product(to_light.direction), 0)
            #specular shading (blinn-phong)
            half_vector = (to_light.direction + to_cam).normalize()
            color += light.color * material.specular * max(normal.dot_product(half_vector), 0) ** specular_k
        return color