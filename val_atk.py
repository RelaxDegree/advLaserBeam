import time
import datetime
import cv2
from PIL import Image
from win10toast import ToastNotifier
from model.test_tf import get_conf
from strategy.particle import advLB

root = 'adv/'
path = 'test.jpg'


def pc_toast():
    toaster = ToastNotifier()
    header = "测试完成"  # 通知的标题
    text = f"{str(datetime.datetime.now())[:-7]}"  # 通知的内容
    time_min = float(0.2)
    time.sleep(1)
    time.sleep(time_min)
    toaster.show_toast(title=f"{header}", msg=f"{text}", duration=10, threaded=True)
    while toaster.notification_active():
        time.sleep(0.001)


# for i in range(100):
img = Image.open(path)
print(get_conf(img))
theta, atk_times = advLB(img, 40, 20, 100)
