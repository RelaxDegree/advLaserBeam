import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models import ResNet50_Weights

from laserBeam.pil_simulation import *

# 加载预训练的ResNet模型
model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()

# 加载ImageNet类别标签
labels_file = "model/imagenet_labels.txt"
with open(labels_file) as f:
    labels = f.readlines()
labels = [label.strip() for label in labels]


def image_load(image_path):
    image = Image.open(image_path)
    return image


# 加载并预处理图像
def get_conf(image, k=5):
    # image = Image.open(image_path)
    # print(type(image))
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # 将图像输入模型并进行预测
    with torch.no_grad():
        output = model(input_batch)

    # 获取预测结果
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    top_k = torch.topk(probabilities, k)

    conf_list = []
    for i in range(k):
        index = top_k.indices[i].item()
        probability = top_k.values[i].item()

        label = labels[index]
        conf_list.append((label, probability))
        # print(f"{label}: {probability:.5f}")
    return conf_list


def get_y_conf(image, label):
    conf_list = get_conf(image, 1000)
    for i in range(len(conf_list)):
        if conf_list[i][0] == label:
            return conf_list[i][1]
    return 0

# initial_model()
# im = Image.open("Line Image.png")
# print(get_conf(im))
