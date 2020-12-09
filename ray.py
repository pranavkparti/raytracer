class Ray:
    """Ray is a half line with origin and normalized direction"""

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
    
    #find position of a point along the ray 
    def at(self, magnitude):
        return self.origin + self.direction * magnitude