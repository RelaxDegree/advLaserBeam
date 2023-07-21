"""
    made by zyh, 2023.7.11
    input a theta and an image, output a new image with laser beam
"""
import math
import random
import time
import aggdraw
from PIL import Image, ImageDraw, ImageFilter
from utils import *
import cv2
import numpy as np

root = '../valdata/'


def trans_image(img, theta):
    img = img.convert("RGBA")
    w, h = img.size[0], img.size[1]
    k = theta.b * theta.alpha * 255
    for i in range(w):
        for j in range(h):
            color = img.getpixel((i, j))
            if color[3] == 0:
                continue
            alpha = int(k / ((1 + (math.tan(theta.l)) ** 2) + theta.b))
            if alpha < 0:
                alpha = 0
            color = color[:-1] + (alpha,)
            img.putpixel((i, j), color)
    return img


def makeLB(vector, image):
    image_width, image_height = image.size[0], image.size[1]
    # 直线的起点和终点坐标
    start_point = (0, int(vector.b))
    end_point = (image_width, int(vector.b + math.tan(vector.l) * image_width))
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.

    draw.line([start_point, end_point], fill=wavelength_to_rgb(vector.phi) + (int(vector.alpha * 255),),
              width=int(vector.w))
    overlay = trans_image(overlay, vector)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1))
    image = image.convert("RGBA")
    result = Image.alpha_composite(image, overlay)
    result = result.convert("RGB")

    return result


#
# image = Image.open(root + 'n0153282900000938.jpg')
# theta = Vector(image)
# theta.print()
# im = makeLB(theta, image)
# im.show()
