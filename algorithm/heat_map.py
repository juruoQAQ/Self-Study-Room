import cv2
import numpy as np
from PIL import Image
from pyheatmap.heatmap import HeatMap
import os


def apply_heatmap(image,data):
    '''image是原图，data是人的中心坐标'''
    '''创建一个新的与原图大小一致的图像，color为0背景为黑色。这里这样做是因为在绘制热力图的时候如果不选择背景图，
    画出来的图与原图大小不一致（根据点的坐标来的），导致无法对热力图和原图进行加权叠加，因此，这里我新建了一张背景图。'''
    background = Image.new("RGB", (image.shape[1], image.shape[0]), color=0)
    # 开始绘制热度图
    hm = HeatMap(data)
    hit_img = hm.heatmap(base=background, r=100)  # background为背景图片，r是半径，默认为10
    hit_img = cv2.cvtColor(np.asarray(hit_img), cv2.COLOR_RGB2BGR)#Image格式转换成cv2格式
    overlay = image.copy()
    alpha = 0.5  # 设置覆盖图片的透明度
    cv2.rectangle(overlay, (0, 0), (image.shape[1], image.shape[0]), (255, 0, 0), -1) # 设置蓝色为热度图基本色蓝色
    image = cv2.addWeighted(overlay, alpha, image, 1-alpha, 0) # 将背景热度图覆盖到原图
    image = cv2.addWeighted(hit_img, alpha, image, 1-alpha, 0) # 将热度图覆盖到原图
    cv2.imshow('heat map',image)
    cv2.waitKey(0)
    return image


# 读取识别后的txt文档
# txt文档所在路径
path_txt = 'lable_result'
#图片所在路径
path_img = 'img_source'
def make_heatmap(path_txt,path_img):
    file_txt = os.listdir(path_txt)
    txt_total = []  # 存储所有路径
    for filename in file_txt:
        first, last = os.path.splitext(filename)
        if last == ".txt":  # 位置文件的后缀名
            txt_total.append(first)
    file_img = os.listdir(path_img)
    img_total = []
    for filename in file_img:
        first, last = os.path.splitext(filename)
        if last == '.jpg':
            img_total.append(first)

    for i in range(0,len(img_total)):
        filename_img = img_total[i]+'.jpg'
        img_path = os.path.join(path_img, filename_img)
        img = cv2.imread(img_path)
        shape = img.shape
        height = shape[0]
        weight = shape[1]
        #  排序文档，也可以不需要看具体情况
        txt_total.sort(key=lambda x: str(x[:-4]))
        print(txt_total)
        data = []
        filename_txt = txt_total[i] + '.txt'
        with open(os.path.join(path_txt, filename_txt), "r+", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.split(" ")
                coordinate = []
                coordinate.append(int(float(line[1]) * weight))
                coordinate.append(int(float(line[2]) * height))
                data.append(coordinate)
                print(data)
        '''cv2.imshow('img', img)
            cv2.waitKey(0)'''
        apply_heatmap(img, data)

make_heatmap(path_txt, path_img)