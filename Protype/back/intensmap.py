import numpy as np
from PIL import Image

class IntensityMap:
    class Mode:
        AVERAGE = 1
        MAX = 2

    def __init__(self, width=None, height=None, rgb_image=None, mode=None, 
                 red_multiplier=1.0, green_multiplier=1.0, blue_multiplier=1.0, alpha_multiplier=0.0):
        if rgb_image is not None:
            self.width, self.height = rgb_image.size
            self.map = self._create_intensity_map(rgb_image, mode, red_multiplier, green_multiplier, blue_multiplier, alpha_multiplier)
        else:
            self.width = width
            self.height = height
            self.map = np.zeros((height, width)) if width and height else None

    def _create_intensity_map(self, image, mode, r_mult, g_mult, b_mult, a_mult):
        image = np.array(image.convert('RGBA'))
        r, g, b, a = image[:,:,0] * r_mult, image[:,:,1] * g_mult, image[:,:,2] * b_mult, image[:,:,3] * a_mult
        
        if mode == IntensityMap.Mode.AVERAGE:
            intensity = (r + g + b + a) / ((r_mult != 0) + (g_mult != 0) + (b_mult != 0) + (a_mult != 0))
        elif mode == IntensityMap.Mode.MAX:
            intensity = np.maximum(np.maximum(r, g), np.maximum(b, a))
        return intensity / 255.0

    def at(self, x, y):
        return self.map[y, x]

    def set_value(self, x, y, value):
        self.map[y, x] = value

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def invert(self):
        self.map = 1.0 - self.map

    def convert_to_qimage(self):
        img = (self.map * 255).astype(np.uint8)
        return Image.fromarray(img, 'L')


