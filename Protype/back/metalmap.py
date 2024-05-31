import numpy as np
from PIL import Image

def create_metallicmap(image_original, contrast=255):
    """
    Genera un mapa metálico a partir de una imagen PIL.

    Args:
        image_original (PIL.Image.Image): Imagen original en formato PIL.
        contrast (int, opcional): Valor de contraste para el mapa metálico. Por defecto es 255.

    Returns:
        PIL.Image.Image: Imagen PIL del mapa metálico generado.
    """
    img = image_original.convert('L')
    img_arr = np.asarray(img)

    metallic = np.zeros_like(img_arr, dtype=np.float32)
    height, width = img_arr.shape
    for y in range(height):
        for x in range(width):
            values = []
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    value = img_arr[(y + dy) % height, (x + dx) % width]
                    values.append(value)
            avg_brightness = np.mean(values)
            metallic[y, x] = 1.0 - avg_brightness / contrast

    metallic /= np.max(metallic)
    out_img = Image.fromarray((metallic * contrast).astype(np.uint8))

    return out_img



