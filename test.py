import os
import random
from util.utils import pc_toast
from strategy.advLB import advLB
from PIL import Image


def testAll(times, root):
    suc = 0
    sum_times = 0
    for i in range(times):
        # 从文件名列表中随机选择一个文件名
        file_names = os.listdir(root)
        random_file_name = random.choice(file_names)
        # 读取图片
        img = Image.open(root + '/' + random_file_name)
        # 获取theta
        theta, atk_times = advLB(img, 40, 20, 100)
        sum_times += atk_times
        if theta is None:
            pc_toast('攻击失败')
            print('攻击失败')
            continue
        suc += 1
        pc_toast('攻击成功')
    pc_toast('成功率: %.5f%% 平均查询次数 %d' % (100 * suc / times, sum_times / suc))


def testOne(root):
    # 对一个图片进行攻击，完成整个PSO并给出分析结果
    file_names = os.listdir(root)
    random_file_name = random.choice(file_names)
    img = Image.open(root + '/' + 'ant__0.9999261.jpg')

    theta, atk_times = advLB_analyze(img, 40, 20, 100)
    if theta is None:
        pc_toast('攻击失败')
        print('攻击失败')
        return
    pc_toast('攻击成功')
    print(theta)


# testOne('highscore')
testAll(10, 'valdata')
