import tkinter as tk
from tkinter import PhotoImage
import cv2
from PIL import Image, ImageTk
import time
from model.test_tf import get_conf
from strategy.particle import advLB
from util.utils import pc_toast
from laserBeam.super_simulation import *

img = None

def adv():
    global img
    root.after_cancel(update_frame.timer_id)
    theta, atk_times = advLB(img, 40, 20, 100)
    if theta is None:
        print('攻击失败')
        return
    img_new = makeLB(theta, img)
    img_new.save('test.jpg')
    img = img_new
    photo = ImageTk.PhotoImage(image=img_new)
    video_label.configure(image=photo)
    video_label.image = photo

def val():
    print(get_conf(img))


def reset():
    update_frame()


def update_frame():
    ret, frame = cap.read()
    if not ret:
        print("无法读取视频帧")
        return
    global img
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = img.resize((960, 540), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image=img)
    video_label.configure(image=photo)
    video_label.image = photo
    timer_id = root.after(10, update_frame)  # 每隔10毫秒更新画面
    update_frame.timer_id = timer_id


url = "http://192.168.50.188:8080//video"

# 创建视频捕捉对象
cap = cv2.VideoCapture(url)

# 检查视频捕捉对象是否成功打开
if not cap.isOpened():
    print("无法打开视频流")
    exit()
start_time = time.time()
root = tk.Tk()
root.title("实时摄像头画面")

video_label = tk.Label(root)
video_label.pack(padx=10, pady=10)

update_frame()
# 创建按钮1
button1 = tk.Button(root, text="计算", command=lambda: adv())
button1.pack(side=tk.LEFT, padx=10)

# 创建按钮2
button2 = tk.Button(root, text="验证", command=lambda: val())
button2.pack(side=tk.LEFT, padx=10)

# 创建按钮3
button3 = tk.Button(root, text="重置", command=lambda: reset())
button3.pack(side=tk.LEFT, padx=10)
root.mainloop()

# 创建一个label框用于显示信息
label = tk.Label(root, text="Hello World!")
label.pack(side=tk.LEFT, padx=10)
# 释放视频捕捉对象和窗口
cap.release()
cv2.destroyAllWindows()
