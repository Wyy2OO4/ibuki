import cv2
from skimage import measure, color
from skimage.measure import regionprops
import numpy as np
import os
import copy


def skimageFilter(gray):
    binary_warped = copy.copy(gray)
    binary_warped[binary_warped > 0.1] = 255
    gray = (np.dstack((gray, gray, gray)) * 255).astype('uint8')
    labels = measure.label(gray[:, :, 0], connectivity=1)
    dst = color.label2rgb(labels, bg_label=0, bg_color=(0, 0, 0))
    gray = cv2.cvtColor(np.uint8(dst * 255), cv2.COLOR_RGB2GRAY)
    return binary_warped, gray


def moveImageTodir(path, targetPath, name):
    if os.path.isdir(path):
        image_name = "gt_image/" + str(name) + ".png"
        binary_name = "gt_binary_image/" + str(name) + ".png"
        instance_name = "gt_instance_image/" + str(name) + ".png"
        train_rows = image_name + " " + binary_name + " " + instance_name + "\n"
        origin_img = cv2.imread(path + "/img.png")
        origin_img = cv2.resize(origin_img, (1280, 720))
        cv2.imwrite(targetPath + "/" + image_name, origin_img)
        img = cv2.imread(path + '/label.png')
        img = cv2.resize(img, (1280, 720))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary_warped, instance = skimageFilter(gray)

        cv2.imwrite(targetPath + "/" + binary_name, binary_warped)
        cv2.imwrite(targetPath + "/" + instance_name, instance)

        print("success创建数据的名称为 : ", train_rows)
        return train_rows
    return None


if __name__ == "__main__":
    count = 0
    with open("./train.txt", 'w+') as file:
        for images_dir in os.listdir("./images"):
            json_dir = os.path.join("./images", images_dir)
            if os.path.isdir(json_dir):
                train_rows = moveImageTodir(json_dir, "./", str(count).zfill(4))
                file.write(train_rows)
                count += 1
        print(f"处理完成，一共处理{count}")