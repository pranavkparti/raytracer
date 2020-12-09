from vector import Color

class Light:
    """Light represents a point light source of a certain color"""

    def __init__(self, position, color=Color.from_hex("#ffffff")):
        self.position = position
        self.color = color