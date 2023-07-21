import math
import random

from PIL import Image, ImageDraw, ImageFilter
import PIL

maxlaserWidth = 20


class Vector:
    def __init__(self, *args):
        if len(args) == 1 and not isinstance(args[0], list):
            image_height = 0
            if isinstance(args[0], PIL.Image.Image):
                image_height = args[0].size[0]
            else:
                image_height = args[0].shape[0]
            lower_bound = 380
            upper_bound = 750
            self.phi = random.gauss((lower_bound + upper_bound) / 2, (upper_bound - lower_bound) / 6)
            self.l = random.uniform(-math.pi + 0.1, math.pi / 2 - 0.1)
            self.l = round(self.l, 5)
            self.b = random.uniform(image_height / 5, image_height * 4 / 5)
            self.w = 10
            self.alpha = random.uniform(0.5, 0.8)
        elif len(args) == 1 and isinstance(args[0], list):
            self.phi = args[0][0]
            self.l = args[0][1]
            self.b = args[0][2]
            self.w = args[0][3]
            self.alpha = args[0][4]
        elif len(args) == 5:
            self.phi = args[0]
            self.l = args[1]
            self.b = args[2]
            self.w = args[3]
            self.alpha = args[4]

    # def __init__(self, phi, l, b, w, alpha):
    #     self.phi = phi
    #     self.l = l
    #     self.b = b
    #     self.w = w
    #     self.alpha = alpha
    def __add__(self, other):
        try:
            return Vector(self.phi + other.phi, self.l + other.l, self.b + other.b, self.w + other.w,
                          self.alpha + other.alpha)
        except:
            self.print()
            other.print()
        # Vector(self.phi + other.phi, self.l + other.l, self.b + other.b, self.w + other.w,
        #        self.alpha + other.alpha)

    def __sub__(self, other):
        try:
            return Vector(self.phi - other.phi, self.l - other.l, self.b - other.b, self.w - other.w,
                          self.alpha - other.alpha)
        except:
            self.print()
            other.print()

    def __mul__(self, size):
        return Vector(self.phi * size, self.l * size, self.b * size, self.w * size, self.alpha)

    def clip(self, image):
        image_height, image_width = image.size[0], image.size[1]
        if self.phi >= 750:
            self.phi = 750
        if self.phi <= 380:
            self.phi = 380
        if self.l >= math.pi / 2:
            self.l = round(self.l, 5)
            self.l -= int(self.l / math.pi + 0.5) * math.pi
            self.l = round(self.l, 5)
        if self.l <= -math.pi / 2:
            self.l = round(self.l, 5)
            self.l += -int(self.l / math.pi - 0.5) * math.pi
            self.l = round(self.l, 5)
        if self.b < 0:
            self.b = 0
        if self.b > image_height:
            self.b = image_height
        if self.w < 10:
            self.w = 10
        if self.w > min(image_width / 20, maxlaserWidth):
            self.w = min(image_width / 20, maxlaserWidth)
        if self.alpha < 0:
            self.alpha = 0
        if self.alpha > 0.7:
            self.alpha = 0.7

    def print(self):
        print('[makeLB phi]', end=' ')
        print(self.phi)
        print('[makeLB l]', end=' ')
        print(self.l)
        print('[makeLB b]', end=' ')
        print(self.b)
        print('[makeLB w]', end=' ')
        print(self.w)
        print('[makeLB alpha]', end=' ')
        print(self.alpha)


# basic
Q = [[80, 0, 0, 0, 0],  # phi
     [0, 0.1, 0, 0, 0],  # l
     [0, 0, 1, 0, 0],  # b
     [0, 0, 0, 2, 0],  # w
     [0, 0, 0, 0, 0.05]]  # alpha

