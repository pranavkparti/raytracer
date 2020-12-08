import math

class Sphere:
    """Sphere is the only 3D shape implemented. Has center, radius, and material"""

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def intersects(self, ray):
        """Checks if ray intersects sphere. Returns distance to intersection or None if no intersection"""
        sphere_to_ray = ray.origin - self.center
        a = 1
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        if discriminant >= 0:
            dist = (-b - math.sqrt(discriminant)) / 2 * a
            if dist > 0:
                return dist