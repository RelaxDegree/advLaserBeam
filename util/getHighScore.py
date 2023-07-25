from model.test_tf import get_conf
import os
import random
from PIL import Image
root = '../valdata/'
times = 100


i = 0
while i < times:
    file_names = os.listdir(root)
    random_file_name = random.choice(file_names)
    img = Image.open(root + random_file_name)
    file_names.remove(random_file_name)
    label, score = get_conf(img)[0]
    if score >= 0.995:
        i += 1
        img.save('../highscore/' + label + '__' + str(score) + '.jpg')
