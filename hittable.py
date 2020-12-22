class Hit_Record:
    def __init__(self, point=None, t=None, normal = None, material=None):
        self.t = t
        self.point = point
        self.normal = normal
        self.material = material

    def set_face_normal(self, ray, outward_normal):
        front_face = ray.direction.dot_product(outward_normal) < 0
        if front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal

# class Hittable:
#     """Abstract class representing any hittable object, say sphere or list of spheres"""
#     def hit(self, ray, tmin, tmax, rec):
#         self.rec = Hit_Record()

