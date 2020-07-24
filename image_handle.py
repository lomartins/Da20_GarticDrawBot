from PIL import Image
import numpy as np

# Paleta de 18 cores do Gartic
gartic_palette = [0, 0, 0,
                  102, 102, 102,
                  0, 0, 255,
                  255, 255, 255,
                  170, 170, 170,
                  0, 255, 255,
                  0, 140, 0,
                  140, 0, 0,
                  140, 69, 0,
                  0, 255, 0,
                  255, 0, 0,
                  255, 127, 0,
                  140, 105, 0,
                  141, 2, 80,
                  141, 105, 103,
                  255, 255, 0,
                  255, 0, 147,
                  255, 193, 191]

# Tabela de Cores do Gartic (gartic_colors.png)
gartic_colors = {'black': (0, 0, 0),            'dark_grey': (0, 0, 40), 'blue': (240, 100, 100),
                'white': (0, 0, 100),           'light_grey': (0, 0, 67),    'light_blue': (180, 100, 100),
                'light_green': (120, 100, 55),  'light_red': (0, 100, 55),   'brown': (30, 100, 55),
                'green': (120, 100, 100),       'red': (0, 100, 100),        'orange': (30, 100, 100),
                'light_yellow': (45, 100, 55),  'light_pink': (326, 99, 55), 'light_salmon': (3, 27, 55),
                'yellow': (60, 100, 100),       'pink': (325, 100, 100),     'salmon': (2, 25, 100)}


class Img:
    def __init__(self):
        self.source = None

    def load(self, image):
        self.source = Image.open(image)

    def to_palette_dict(self):
        palette_img = Image.new('P', (16, 16))
        palette_img.putpalette(gartic_palette * int(256 / (len(gartic_palette) / 3)))

        processed_img = image_processing(self.source)

        new_image = quantize_to_palette(processed_img, palette_img, dither=False)
        new_image = new_image.convert('RGB')
        new_image.save('./scaled.png')

        width, height = new_image.size

        image_map_color = {}

        for y in range(height):
            for x in range(width):
                pixel = new_image.getpixel((x, y))
                rgb = "%d,%d,%d" % ((pixel[0]), (pixel[1]), (pixel[2]))
                pixel_i = "%d_%d" % (x, y)

                if rgb not in image_map_color.keys():
                    image_map_color[rgb] = []

                image_map_color[rgb].append((x*3, y*3))

        return image_map_color


def image_processing(img):
    resized_img = img.resize((32, 32), Image.ANTIALIAS)
    rgba_img = resized_img.convert('RGBA')
    processed_img = whiten_background(rgba_img).convert('RGB')
    return processed_img


def whiten_background(img):
    fill_color = (255, 255, 255)
    if img.mode in ('RGBA', 'LA'):
        background = Image.new(img.mode[:-1], img.size, fill_color)
        background.paste(img, img.split()[-1])  # omit transparency
        return background


def load_image(image_path):
    loaded = Img()
    loaded.load(image_path)
    return loaded


def quantize_to_palette(image, palette, dither=False):
    # Convert an RGB or L mode image to use a given P image's palette.
    image.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if image.mode != "RGB" and image.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = image.im.convert("P", 1, palette.im)
    # the 0 above means turn OFF dithering

    try:
        return image._new(im)
    except AttributeError:
        return image._makeself(im)
