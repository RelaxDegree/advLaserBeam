import math
from PIL import Image
import PIL
from theta import Vector
from util.utils import *
import cv2
import numpy as np
root = '../valdata/'


def makeLB(vector, img):
    if isinstance(img, PIL.Image.Image):
        img = np.array(img)
    image_width, image_height = img.shape[1], img.shape[0]
    start_point = (0, int(vector.b))
    end_point = (image_width, int(vector.b + math.tan(vector.l) * image_width))
    mask_image = img.copy()
    cv2.line(mask_image, start_point, end_point, wavelength_to_rgb(vector.phi), thickness=int(vector.w),
             lineType=cv2.LINE_AA)

    result = cv2.addWeighted(mask_image, vector.alpha, img, 1 - vector.alpha, 0)
    cv2.imshow('Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result = Image.fromarray(result)
    return result


image = cv2.imread(root + 'n0153282900000938.jpg')
theta = Vector(image)
im = makeLB(theta, image)
im.show()