import time
import datetime
import cv2
from PIL import Image
from win10toast import ToastNotifier
from model.test_tf import get_conf
from strategy.particle import advLB

root = 'adv/'
path = 'test.jpg'


img = Image.open(path)
print(get_conf(img))
theta, atk_times = advLB(img, 40, 20, 100)
