import numpy as np
from PIL import Image

class IntensityBumpMap:
    class Mode:
        AVERAGE = 0
        MAX = 1

    def __init__(self, width=None, height=None, rgb_image=None, mode=None, red_multiplier=1.0, green_multiplier=1.0, blue_multiplier=1.0, alpha_multiplier=0.0):
        if rgb_image:
            self.map = self._create_intensity_map(rgb_image, mode, red_multiplier, green_multiplier, blue_multiplier, alpha_multiplier)
        else:
            self.map = np.zeros((height, width))

    def _create_intensity_map(self, rgb_image, mode, red_multiplier, green_multiplier, blue_multiplier, alpha_multiplier):
        rgb_image = rgb_image.convert('RGBA')
        width, height = rgb_image.size
        intensity_map = np.zeros((height, width))
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = rgb_image.getpixel((x, y))
                r *= red_multiplier
                g *= green_multiplier
                b *= blue_multiplier
                a *= alpha_multiplier
                
                if mode == self.Mode.AVERAGE:
                    intensity = (r + g + b + a) / (red_multiplier + green_multiplier + blue_multiplier + alpha_multiplier)
                elif mode == self.Mode.MAX:
                    intensity = max(r, g, b, a)
                
                intensity_map[y, x] = intensity
        
        return intensity_map

    def at(self, x, y):
        return self.map[y, x]
    
    def set_value(self, x, y, value):
        self.map[y, x] = value

    def get_width(self):
        return self.map.shape[1]

    def get_height(self):
        return self.map.shape[0]
    
    def invert(self):
        self.map = 255 - self.map
    
    def convert_to_qimage(self):
        return Image.fromarray(self.map).convert('L')
