import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
model = ResNet50(weights='imagenet')
image_paths = ['adv/Afghan_hound--mortarboard--0.0028103534.jpg', 'adv/African_hunting_dog--plow--0.0012831268.jpg']
images = []

# 逐个加载和预处理图像
for path in image_paths:
    img = image.load_img(path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    images.append(img)

# 创建包含所有图像的数组
images = np.concatenate(images, axis=0)
predictions = model.predict(images)

# 解码预测结果
decoded_predictions = decode_predictions(predictions, top=3)

# 输出预测结果
for i, preds in enumerate(decoded_predictions):
    print("Predictions for image", i+1)
    for pred in preds:
        print(pred)
    print()
