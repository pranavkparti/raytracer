from vector import Color
from sphere import Sphere
from ray import Ray
from collections import namedtuple

# class Material:
#     """Material has color and properties that define how it reacts to light"""

    # def __init__(self, color=Color.from_hex("#ffffff"), attenuation=0.5):
    #     self.attenuation = attenuation
    #     self.color = color

#     def __init__(self, color=Color.from_hex("#ffffff"), ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5):
#         self.color = color
#         self.ambient = ambient
#         self.diffuse = diffuse
#         self.specular = specular
#         self.reflection = reflection

#     def color_at(self, position):
#         return self.color
        

# class ChequeredMaterial:
#     """Material with a chessboard patternof two colors"""

#     def __init__(self, color1=Color.from_hex("#ffffff"), color2=Color.from_hex("#000000"), ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5):
#         self.color1 = color1
#         self.color2 = color2
#         self.ambient = ambient
#         self.diffuse = diffuse
#         self.specular = specular
#         self.reflection = reflection
    
#     def color_at(self, position):
#         if int((position.x + 5.0) * 3.0) % 2 == int(position.z * 3.0) % 2:
#             return self.color1
#         else:
#             return self.color2
        
    # def scatter(self, r_in, rec, attentuation, scattered):
    #     pass

ScatterInfo = namedtuple('ScatterInfo', ['scattered', 'attenuation'])

class Material:
    def scatter(self, ray, hit_info):
        raise NotImplementedError

class Lambertian(Material):
    def __init__(self, albedo):
        super().__init__()
        self.albedo = albedo

    def scatter(self, ray, hit_info):
        target = hit_info.point + hit_info.normal + Sphere.random_in_unit_sphere()
        scattered = Ray(hit_info.point, target - hit_info.point)
        attenuation = self.albedo

        return ScatterInfo(scattered, attenuation)

def reflect(v, n):
    return v - 2*v.dot_product(n)*n

class Metal(Material):
    def __init__(self, albedo, fuzz=0):
        super().__init__()
        self.albedo = albedo

        # fuzz is the fuzziness or perturbation parameter
        # it determines the fuzziness of the reflections
        self.fuzz = min(1, max(0, fuzz)) # ensures 0 <= self.fuzz <= 1

    def scatter(self, ray, hit_info):
        # Idea: Make ray.direction a computed property that returns the
        # unit direction vector when first accessed
        # maybe call it unit_direction and leave direction unchanged
        reflected = reflect(ray.direction.normalize(), hit_info.normal)
        scattered = Ray(hit_info.point, reflected + self.fuzz * Sphere.random_in_unit_sphere())
        attenuation = self.albedo

        if scattered.direction.dot_product(hit_info.normal) > 0:
            return ScatterInfo(scattered, attenuation)

        return None