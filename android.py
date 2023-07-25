import time
import cv2
from PIL import Image
from model.test_tf import *
from strategy.particle import advLB
# IP Webcam的视频流地址
url = "http://192.168.50.188:8080//video"

# 创建视频捕捉对象
cap = cv2.VideoCapture(url)

# 检查视频捕捉对象是否成功打开
if not cap.isOpened():
    print("无法打开视频流")
    exit()

# 创建窗口
cv2.namedWindow("Camera Stream", cv2.WINDOW_NORMAL)

# 初始化帧数和计时器
fps = 0
start_time = time.time()
threshold = 100  # 根据实际情况调整阈值


def calculate(image1, image2):
    # 灰度直方图算法
    # 计算单通道的直方图的相似值

    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                     (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def classify_hist_with_split(image1, image2, size=(256, 256)):
    # RGB每个通道的直方图相似度
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data

# ======================================================================================================================
import tkinter as tk
from PIL import Image, ImageTk

def adv(img):
    img = img.resize((400, 300), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    image_label.configure(image=photo)
    image_label.image = photo

# 创建主窗口
root = tk.Tk()
root.title("camera")

# 创建图像框
image_label = tk.Label(root, width=400, height=300, borderwidth=2, relief="solid")
image_label.pack(pady=20)

# 创建按钮1
button1 = tk.Button(root, text="计算", command=lambda: adv())
button1.pack(side=tk.LEFT, padx=10)

# 创建按钮2
button2 = tk.Button(root, text="重置", command=lambda: change_image("image2.jpg"))
button2.pack(side=tk.LEFT, padx=10)
# 显示默认图像
default_image = Image.open("sin_function.png")
default_image = default_image.resize((600, 450), Image.ANTIALIAS)
default_photo = ImageTk.PhotoImage(default_image)
image_label.configure(image=default_photo)
image_label.image = default_photo

# 运行主循环
root.mainloop()
# ======================================================================================================================
while True:
    # 读取视频帧
    ret, frame = cap.read()

    # 检查视频帧是否成功读取
    if not ret:
        print("无法读取视频帧")
        break

    # 在窗口中显示视频帧


    if time.time() - start_time >= 1:
        cv2.imshow("Camera Stream", frame)
        # 加载两个待比较的图片
        # img为之前使用cv2读取的图片数据
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        print(get_conf(img))
        start_time = time.time()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放视频捕捉对象和窗口
cap.release()
cv2.destroyAllWindows()