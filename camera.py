from vector import Point, Vector

class Camera:
    def __init__(self, viewport_height, aspect_ratio):
        self.viewport_height = viewport_height
        self.viewport_width = viewport_height * aspect_ratio

        #fixed value, for now
        self.focal_length = 1.0 
        self.origin = Point(0,0,0)
        self.horizontal = Vector(self.viewport_width, 0, 0)
        self.vertical = Vector(0, self.viewport_height, 0)
        self.lower_left_corner = (self.origin 
                                    - self.horizontal / 2 
                                    - self.vertical / 2 
                                    - Vector(0, 0, self.focal_length)
                                    )
        

        