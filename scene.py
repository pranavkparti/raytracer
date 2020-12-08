class Scene:
    """Scene has all information needed for the engine to render"""

    def __init__(self, camera, objects, width, height):
        self.camera = camera
        self.objects = objects
        self.width = width
        self.height = height
        