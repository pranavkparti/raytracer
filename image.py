class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]
    
    def set_pixel(self, x, y, col):
        self.pixels[y][x] = col

    def write_ppm(self, img_fileobj):
        Image.write_ppm_header(img_fileobj, height=self.height, width=self.width)
        self.write_ppm_raw(img_fileobj)


    @staticmethod
    def write_ppm_header(image_fileobj, height=None, width=None):
        """Writes only header of a PPM file"""
        
        #image header
        image_fileobj.write('P3 {} {}\n255\n'.format(width, height))


    def write_ppm_raw(self, img_fileobj):
        def to_byte(c):
            return round(max(min(c * 255, 255), 0)) #setting possible range for c, i.e, 0 to 255 

        for row in self.pixels:
            for color in row:
                img_fileobj.write(
                    "{} {} {} ".format(
                        to_byte(color.x), to_byte(color.y), to_byte(color.z)
                    )
                )
            img_fileobj.write('\n')

