"""
    made by zyh, 2023.7.11
    input a label and an image, output a list of score and label, or 0 if not found
"""
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from PIL import Image

# 加载预训练的 ResNet-50 模型
# model = ResNet50(weights='imagenet')
model = MobileNetV2(weights='imagenet')


# def model_load():
#     model = ResNet50(weights='imagenet')
#     return model


def image_load(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    return img


def get_conf(img, k=5, ):
    img = img.resize((224, 224))
    # img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    # 使用模型进行预测
    preds = model.predict(x)
    # 解码预测结果
    decoded_preds = decode_predictions(preds, top=k)[0]
    # 打印预测结果
    conf_list = []
    for class_id, class_name, probability in decoded_preds:
        conf_list.append((class_name, probability))
    del img, x, preds, decoded_preds
    return conf_list


def get_y_conf(image, label):
    conf_list = get_conf(image, 1000)
    del image
    for i in range(len(conf_list)):
        if conf_list[i][0] == label:
            return conf_list[i][1]
    return 0


# def get_conf(images):
#     images = np.concatenate(images, axis=0)
#     predictions = model.predict(images)
#     # 解码预测结果
#     decoded_predictions = decode_predictions(predictions, top=3)
#     # 输出预测结果
#     label_conf_list = []
#     for i, preds in enumerate(decoded_predictions):
#         # print(preds)
#         label_conf_list.append((preds[0][1], preds[0][2], preds[1][2]))
#     return label_conf_list
