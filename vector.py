import math

class Vector():
    """A three element vector used in 3D graphics for multiple purposes"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    #operator overloading
    
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)

    #overloaded for unary negative -
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    def __mul__(self, other):
        assert not isinstance(other, Vector)
        return Vector(self.x*other, self.y*other, self.z*other) #vector multiplied with a constant

    def __rmul__(self, other):
        return self.__mul__(other) #it's commutative after all
    
    def __truediv__(self, other):
        assert not isinstance(other, Vector)
        return Vector(self.x/other, self.y/other, self.z/other) #vector divided with a constant

    #dot product of two vectors
    def dot_product(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    #cross product of two vectors
    def cross_product(self, other):
        return Vector(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
                )

    def magnitude(self):
        return math.sqrt(self.dot_product(self))

    #normalized, i.e, unit vector
    def normalize(self):
        return self / self.magnitude()

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z) #could also use f string

class Color(Vector):
    """Stores color as RGB triplets. Alias for Vector"""
    
    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)

class Point(Vector):
    """Point stores the 3D coordinates. Alias for Vector"""
    pass