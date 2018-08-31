from PIL import Image
import random
def crop(screenshot, parsed, path):
    im = Image.open(screenshot)  # uses PIL library to open image in memory
    location = parsed['location']
    size = parsed['size']
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save(path)  # saves new cropped image