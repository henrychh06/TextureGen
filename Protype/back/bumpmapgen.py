from PIL import Image
import numpy as np
from intensBump import IntensityBumpMap

class BumpmapGenerator:
    def __init__(self, mode, red_multiplier, green_multiplier, blue_multiplier, alpha_multiplier):
        self.mode = mode
        self.red_multiplier = red_multiplier
        self.green_multiplier = green_multiplier
        self.blue_multiplier = blue_multiplier
        self.alpha_multiplier = alpha_multiplier

    def calculate_bumpmap(self, input_image):
        input_image = input_image.convert('RGBA')
        width, height = input_image.size
        intensity_map = IntensityBumpMap(rgb_image=input_image, mode=self.mode, 
                                     red_multiplier=self.red_multiplier, 
                                     green_multiplier=self.green_multiplier,
                                     blue_multiplier=self.blue_multiplier, 
                                     alpha_multiplier=self.alpha_multiplier)
        
        bumpmap = Image.new('L', (width, height))
        bumpmap_data = np.zeros((height, width), dtype=np.uint8)
        
        for y in range(height):
            for x in range(width):
                intensity = intensity_map.at(x, y)
                bumpmap_data[y, x] = int(intensity)
        
        bumpmap = Image.fromarray(bumpmap_data, 'L')
        return bumpmap
