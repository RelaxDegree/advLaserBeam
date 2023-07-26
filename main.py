import tkinter as tk
from tkinter import PhotoImage
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
import time
from model.test_tf import get_conf
from strategy.particle import advLB
from util.utils import pc_toast
from laserBeam.super_simulation import *
from laserBeam.theta_constraint import set_laser

img = None


def show_image_window(image, text):
    # 创建新的Toplevel窗口
    image_window = tk.Toplevel(root)
    image_window.title(text)
    # 显示图片
    image_label = tk.Label(image_window)
    image_label.pack()
    photo = ImageTk.PhotoImage(image=image)
    image_label.configure(image=photo)
    image_label.image = photo


def adv():
    global img
    root.after_cancel(update_frame.timer_id)
    theta, atk_times = advLB(img, 40, 20, 100)
    if theta is None:
        print('攻击失败')
        return
    img_new = makeLB(theta, img)
    show_image_window(img_new, "攻击后图片")
    # img.show()
    # photo = ImageTk.PhotoImage(image=img_new)
    # video_label.configure(image=photo)
    # video_label.image = photo


def val():
    print(get_conf(img))
    show_image_window(img,"测试图片")

def reset():
    global cap
    cap = cv2.VideoCapture(url)
    update_frame()


def update_frame():
    ret, frame = cap.read()
    if not ret:
        print("无法读取视频帧")
        return
    global img
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = img.resize((1152, 648), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image=img)
    video_label.configure(image=photo)
    video_label.image = photo
    timer_id = root.after(10, update_frame)  # 每隔10毫秒更新画面
    update_frame.timer_id = timer_id


def update_setting():
    if phi_entry.get() == '' or width_entry.get() == '' or alpha_entry.get() == '':
        messagebox.showwarning("警告", "请输入参数")
        return
    set_laser(phi_entry.get(), width_entry.get(), alpha_entry.get())


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

laser_phi = tk.Label(root, text="波长:")
laser_phi.pack(side=tk.LEFT, padx=10)
phi_entry = tk.Entry(root)
phi_entry.pack(side=tk.LEFT, padx=10)
laser_width = tk.Label(root, text="宽度:")
laser_width.pack(side=tk.LEFT, padx=10)
width_entry = tk.Entry(root)
width_entry.pack(side=tk.LEFT, padx=10)
laser_alpha = tk.Label(root, text="强度:")
laser_alpha.pack(side=tk.LEFT, padx=10)
alpha_entry = tk.Entry(root)
alpha_entry.pack(side=tk.LEFT, padx=10)
# 创建按钮4
button4 = tk.Button(root, text="设置", command=lambda: update_setting())
button4.pack(side=tk.LEFT, padx=10)
root.mainloop()

# 释放视频捕捉对象和窗口
cap.release()
cv2.destroyAllWindows()
