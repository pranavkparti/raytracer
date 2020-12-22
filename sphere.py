import math
from hittable import Hit_Record
from vector import Vector
from random import random, uniform

class Sphere():
    """Sphere is the only 3D shape implemented. Has center, radius, and material"""

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def intersects(self, ray, tmin, tmax):
        sphere_to_ray = ray.origin - self.center
        a = 1 #basically, ray.direction.dot_product(ray.direction)
        half_b = ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        rec = Hit_Record()

        if discriminant >= 0:
            dist = (-half_b - math.sqrt(discriminant)) / a
            if dist < tmin or tmax < dist:
                dist = (-half_b + math.sqrt(discriminant)) / a
                if dist < tmin or tmax < dist:
                    return None
            rec.t = dist
            rec.point = ray.at(rec.t)
            outward_normal = (rec.point - self.center) / self.radius
            rec.normal = self.set_face_normal(ray, outward_normal)
            rec.material = self.material
            return rec #define rec here instead, as in send the values to engine
        else:
            return None
    # def intersects(self, ray):
    #     """Checks if ray intersects sphere. Returns distance to intersection or None if no intersection"""
    #     sphere_to_ray = ray.origin - self.center
    #     a = 1 #basically, ray.direction.dot_product(ray.direction)
    #     #b = 2 * ray.direction.dot_product(sphere_to_ray)
    #     half_b = ray.direction.dot_product(sphere_to_ray)
    #     c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
    #     #discriminant = b * b - 4 * a * c
    #     discriminant = half_b * half_b - a * c

    #     if discriminant >= 0:
    #         #dist = (-b - math.sqrt(discriminant)) / 2 * a
    #         dist = (-half_b - math.sqrt(discriminant)) / a
    #         if dist > 0:
    #             return dist
    
    def normal(self, surface_point):
        """Returns surface normal to the point on the sphere's surface"""

        return (surface_point - self.center).normalize()
    
    def set_face_normal(self, ray, outward_normal):
        front_face = ray.direction.dot_product(outward_normal) < 0
        if front_face:
            normal = outward_normal
        else:
            normal = -outward_normal
        return normal
    
    @classmethod
    def random_in_unit_sphere(self):
        while 1:
            p = Vector(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))
            if p.magnitude() >= 1:
                continue
            else:
                return p
    @classmethod
    def random_unit_vector(self):
        return self.random_in_unit_sphere().normalize()

