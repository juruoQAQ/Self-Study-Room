import cv2
import numpy as np
from PIL import Image
from pyheatmap.heatmap import HeatMap


def apply_heatmap(image,data):
    '''image是原图，data是人的中心坐标'''
    '''创建一个新的与原图大小一致的图像，color为0背景为黑色。这里这样做是因为在绘制热力图的时候如果不选择背景图，画出来的图与原图大小不一致（根据点的坐标来的），导致无法对热力图和原图进行加权叠加，因此，这里我新建了一张背景图。'''
    background = Image.new("RGB", (image.shape[1], image.shape[0]), color=0)
    # 开始绘制热度图
    hm = HeatMap(data)
    hit_img = hm.heatmap(base=background, r = 100) # background为背景图片，r是半径，默认为10
    hit_img = cv2.cvtColor(np.asarray(hit_img),cv2.COLOR_RGB2BGR)#Image格式转换成cv2格式
    overlay = image.copy()
    alpha = 0.5 # 设置覆盖图片的透明度
    cv2.rectangle(overlay, (0, 0), (image.shape[1], image.shape[0]), (255, 0, 0), -1) # 设置蓝色为热度图基本色蓝色
    image = cv2.addWeighted(overlay, alpha, image, 1-alpha, 0) # 将背景热度图覆盖到原图
    image = cv2.addWeighted(hit_img, alpha, image, 1-alpha, 0) # 将热度图覆盖到原图
    cv2.imshow('heat map',image)