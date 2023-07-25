"""
    made by zyh, 2023.7.11
    input a theta and an image, output a new image with laser beam
"""
import math
import aggdraw
from PIL import Image
from util.utils import *
from theta import Vector

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
    result = image.copy()
    k = math.tan(vector.l)
    b = vector.b
    beta = 9
    alpha = vector.alpha
    light_end_y = int(math.sqrt(beta * 20) + 0.5)
    full_light_end_y = int(math.sqrt(beta) + 0.5)
    color = wavelength_to_rgb(vector.phi)
    image_width, image_height = image.size[0], image.size[1]
    layout = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
    # 直线的起点和终点坐标
    start_point = (0, int(vector.b))
    end_point = (image_width, int(vector.b + math.tan(vector.l) * image_width))
    draw = aggdraw.Draw(layout)
    pen = aggdraw.Pen(color + (int(vector.alpha * 255),), int(vector.w))
    draw.line((start_point[0], start_point[1], end_point[0], end_point[1]), pen)
    draw.flush()

    # for x in range(image_width):
    #     for y in range(image_height):
    #         distance = abs(k * x - y + b) / math.sqrt(1 + k * k)
    #         if distance < 0:
    #             print(distance)
    #         if distance <= full_light_end_y:
    #             layout[y, x, 0] = color[0] * alpha
    #             layout[y, x, 1] = color[1] * alpha
    #             layout[y, x, 2] = color[2] * alpha
    #         elif full_light_end_y < distance <= light_end_y:
    #             attenuation = beta / (distance * distance)
    #             layout[y, x, 0] = color[0] * alpha * attenuation
    #             layout[y, x, 1] = color[1] * alpha * attenuation
    #             layout[y, x, 2] = color[2] * alpha * attenuation
    return layout


image = Image.open(root + 'n0153282900000938.jpg')
theta = Vector(image)
theta.alpha = 0.3
theta.print()
im = makeLB(theta, image)
im.show()
