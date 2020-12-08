from image import Image
from ray import Ray
from point import Point
from color import Color

class RenderEngine:
    """Renders 2D objects into 3D objectys using ray tracing"""

    def render(self, scene):
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
        pixels = Image(width, height)

        for j in range(height):
            y = y0 + j * ystep
            for i in range(width):
                x = x0 + i * xstep
                ray = Ray(camera, Point(x, y) - camera)
                pixels.set_pixel(i, j, self.ray_trace(ray, scene))
        return pixels

    def ray_trace(self, ray, scene):
        color = Color(0,0,0)
        #find nearest object to ray in the scene
        dist_hit, object_hit = self.find_nearest(ray, scene)
        if object_hit is None:
            return color
        hit_pos = ray.origin + ray.direction * dist_hit
        color += self.color_at(object_hit, hit_pos, scene)
        return color

    def find_nearest(self, ray, scene):
        dist_min = None
        obj_hit = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)


    def color_at(self, obj_hit, hit_pos, scene):
        return obj_hit.material