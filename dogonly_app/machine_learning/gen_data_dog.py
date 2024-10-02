from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection

parent_directory = "./photos/"
categories = ['dog', 'another']

num_classes = len(categories)
image_size = 50
num_testdata = 80

min_num_images = min(len(glob.glob(os.path.join(parent_directory, category, '*/*.jpg'))) for category in categories)

# 画像の読み込み
X_train = []
X_test = []
Y_train = []
Y_test = []

for category_index, category in enumerate(categories):
    sub_classes = [os.path.join(parent_directory, category, folder) for folder in os.listdir(os.path.join(parent_directory, category)) if os.path.isdir(os.path.join(parent_directory, category, folder))]

    for sub_class in sub_classes:
        files = glob.glob(sub_class + "/*.jpg")
        for i, file in enumerate(files):
            if i >= min_num_images:
                break
            image = Image.open(file)
            image = image.convert("RGB")
            image = image.resize((image_size, image_size))
            data = np.asarray(image)

            if i < num_testdata:
                X_test.append(data)
                Y_test.append(category_index)  # dogなら0、anotherなら1
            else:
                for angle in range(-20, 20, 5):
                    # 回転
                    img_r = image.rotate(angle)
                    data = np.asarray(img_r)
                    X_train.append(data)
                    Y_train.append(category_index)  # dogなら0、anotherなら1
                    # 反転
                    img_trans = img_r.transpose(Image.FLIP_LEFT_RIGHT)
                    data = np.asarray(img_trans)
                    X_train.append(data)
                    Y_train.append(category_index)  # dogなら0、anotherなら1

# numpy配列に変換
X_train = np.array(X_train)
X_test = np.array(X_test)
Y_train = np.array(Y_train)
Y_test = np.array(Y_test)

# データを保存
xy = (X_train, X_test, Y_train, Y_test)
np.save("./dog_or_not.npy", xy)
