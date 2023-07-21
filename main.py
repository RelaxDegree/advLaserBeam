import os
import random
from utils import pc_toast
from strategy.particle import advLB
from PIL import Image

folder_path = 'valdata'  # 替换为你的文件夹路径
times = 30
suc = 0
sum_times = 0
for i in range(times):
    # 从文件名列表中随机选择一个文件名
    file_names = os.listdir(folder_path)
    random_file_name = random.choice(file_names)
    # 读取图片
    img = Image.open(folder_path + '/' + random_file_name)
    # 获取theta
    theta, atk_times = advLB(img, 40, 20, 100)
    sum_times += atk_times
    if theta is None:
        pc_toast('攻击失败')
        print('攻击失败')
        continue
    suc += 1
    pc_toast('攻击成功')
pc_toast('成功率: %f 平均查询次数 %d' % (100 * suc / times, sum_times / suc))
