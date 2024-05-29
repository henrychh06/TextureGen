import numpy as np
from PIL import Image
from intensmap import IntensityMap

class SpecularmapGenerator:
    def __init__(self, mode, red_multiplier, green_multiplier, blue_multiplier, alpha_multiplier):
        self.mode = mode
        self.red_multiplier = red_multiplier
        self.green_multiplier = green_multiplier
        self.blue_multiplier = blue_multiplier
        self.alpha_multiplier = alpha_multiplier

    def calculate_specmap(self, input_image, scale, contrast):
        input_image = input_image.convert('RGBA')
        width, height = input_image.size
        result = Image.new('RGBA', (width, height))
        
        contrast_lookup = self._create_contrast_lookup(contrast)
        input_intensity = IntensityMap(rgb_image=input_image, mode=self.mode, 
                                       red_multiplier=self.red_multiplier, 
                                       green_multiplier=self.green_multiplier,
                                       blue_multiplier=self.blue_multiplier, 
                                       alpha_multiplier=self.alpha_multiplier)

        multiplier_sum = sum([self.red_multiplier != 0.0, self.green_multiplier != 0.0, 
                              self.blue_multiplier != 0.0, self.alpha_multiplier != 0.0])
        if multiplier_sum == 0.0:
            multiplier_sum = 1.0
        
        input_array = np.array(input_image)
        result_array = np.zeros_like(input_array)
        
        for y in range(height):
            for x in range(width):
                intensity = input_intensity.at(x, y) / multiplier_sum
                intensity *= scale
                intensity = min(1.0, max(0.0, intensity))
                c = int(255.0 * intensity)
                c = contrast_lookup[c]
                result_array[y, x] = [c, c, c, input_array[y, x, 3]]
        
        return Image.fromarray(result_array, 'RGBA')

    def _create_contrast_lookup(self, contrast):
        contrast_lookup = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            new_value = (i / 255.0 - 0.5) * contrast + 0.5
            new_value = min(255, max(0, int(new_value * 255)))
            contrast_lookup[i] = new_value
        return contrast_lookup
