import cv2.cv2 as cv2
import os
import json
import numpy as np


def get_seats(reserved_number, empty_number):  # 获取预约位置的坐标信息
    with open('seats.json', 'r') as f:
        content = f.read()
        all_seats = json.loads(content)
    reserved_seats = []
    empty_seats = []

    for i in range(len(reserved_number)):
        if str(reserved_number[i]) in all_seats.keys():
            seat = all_seats[str(reserved_number[i])]
            reserved_seats.append([str(reserved_number[i]), seat['x'], seat['y'], seat['width'], seat['height']])

    for i in range(len(empty_number)):
        if str(empty_number[i]) in all_seats.keys():
            seat = all_seats[str(empty_number[i])]
            empty_seats.append([str(empty_number[i]), seat['x'], seat['y'], seat['width'], seat['height']])
    return reserved_seats, empty_seats


def get_coordinate(height, width, array, para):
    coordinates = []
    para = 1.0 - para
    for i in range(len(array)):
        x = height * (float(array[i][2]))
        y = width * (float(array[i][1]))
        h = height * (float(array[i][4]))
        w = width * (float(array[i][3]))
        xvar = w * para
        yvar = h * para
        ymin = int(x - h / 2 + yvar)
        xmin = int(y - w / 2 + xvar)
        ymax = int(x + h / 2 - yvar)
        xmax = int(y + w / 2 - xvar)
        coordinates.append([array[i][0], xmin, ymin, xmax, ymax])
    return coordinates


def cal_iou(bbox1, bbox2):
    xmin1, ymin1, xmax1, ymax1 = bbox1
    xmin2, ymin2, xmax2, ymax2 = bbox2

    xx1 = np.max([xmin1, xmin2])
    yy1 = np.max([ymin1, ymin2])
    xx2 = np.min([xmax1, xmax2])
    yy2 = np.max([ymax1, ymax2])

    aera1 = (xmax1 - xmin1) * (ymax1 - ymin1)
    aera2 = (xmax2 - xmin2) * (ymax2 - ymin2)

    inter_aera = (np.max([0, xx2 - xx1])) * (np.max([0, yy2 - yy1]))
    iou = inter_aera / (aera1 + aera2 - inter_aera + 1e-6)
    return iou


def is_center(bbox1, bbox2):
    if bbox1[0] >= bbox2[0] and bbox1[1] >= bbox2[1] and bbox1[2] <= bbox2[2] and bbox1[3] <= bbox2[3]:
        return True
    return False


def detect(img_path, reserved_seats, empty_seats):
    reserved_locations, empty_locations = get_seats(reserved_seats, empty_seats)  # 读取json,获取座位列表
    os.system("python detect.py --save-txt  --exist-ok --hide-labels --source {}".format(img_path))  # 进行检测，得到检测结果
    img_name = os.path.basename(img_path)  # 图片名
    detected_img_path = 'runs/detect/exp/{}'.format(img_name)  # 检测结果图片路径
    detected_img = cv2.imread(detected_img_path)  # 读取图片
    size = detected_img.shape
    h = size[0]
    w = size[1]
    img_name_pre = img_name.split('.')[0]
    head_txt_path = 'runs/detect/exp/labels/{}.txt'.format(img_name_pre)  # 检测结果坐标路径
    head_array = []
    head_count = 0
    with open(head_txt_path) as file:  # 打开检测结果坐标路径
        for line in file:
            str_list = line.split()
            head_array.append(str_list)
            head_count += 1
    head_locations = get_coordinate(h, w, head_array, 0.4)  # 获取人头中心坐标
    reserved_locations = get_coordinate(h, w, reserved_locations, 1.0)  # 获取预约座位坐标
    empty_locations = get_coordinate(h, w, empty_locations, 1.0)  # 获取空置座位坐标
    empty_seats_number = []  # 预约但无人座位号
    occupied_seats_number = []  # 有人但无预约座位号

    # 对每个预约座位进行遍历，如果无人就画框并记录座位号
    for i in range(len(reserved_locations)):
        max_iou = 0
        head_number = 0
        for j in range(len(head_locations)):
            iou = cal_iou(head_locations[j][1:5], reserved_locations[i][1:5])
            if iou > max_iou:
                max_iou = iou
                head_number = j

        have_head = is_center(head_locations[head_number][1:5], reserved_locations[i][1:5])

        if not have_head:
            cv2.rectangle(detected_img, (reserved_locations[i][1], reserved_locations[i][2]),
                          (reserved_locations[i][3], reserved_locations[i][4]), (0, 255, 0), 1)
            text = reserved_locations[i][0]
            empty_seats_number.append(text)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(detected_img, text, (reserved_locations[i][1], reserved_locations[i][2]),
                        font, 0.3, (0, 0, 255), 1)

    # 对每个空置座位框进行遍历，如果有人就画框并记录座位号
    for i in range(len(empty_locations)):
        head_appear = False
        for j in range(len(head_locations)):
            if (head_locations[j][1] >= empty_locations[i][1] and head_locations[j][2] >= empty_locations[i][2]
                    and head_locations[j][3] <= empty_locations[i][3] and head_locations[j][4] <= empty_locations[i][4]):
                head_appear = True
                break
        if head_appear:
            cv2.rectangle(detected_img, (empty_locations[i][1], empty_locations[i][2]),
                          (empty_locations[i][3], empty_locations[i][4]), (205, 0, 0), 1)
            text = empty_locations[i][0]
            occupied_seats_number.append(text)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(detected_img, text, (empty_locations[i][1], empty_locations[i][2]), font, 0.3, (0, 0, 255), 1)

    if os.path.exists(head_txt_path):
        os.remove(head_txt_path)
    return detected_img, empty_seats_number, occupied_seats_number, head_count


if __name__ == '__main__':
    iou = cal_iou([0, 0, 100, 100], [100, 100, 500, 500])
    img = 'data/images/studyroom.png'
    reserved_seat = list(range(200, 300))
    # empty_seat = [231, 239, 242, 256, 259, 268, 277]
    empty_seat = [276]
    # empty_seat = list(range(200, 350))
    detected, empty_numbers, occupied_numbers, counts = detect(img, reserved_seat, empty_seat)  # 检测
    print(empty_numbers, occupied_numbers, counts)
    cv2.imshow("test", detected)
    cv2.waitKey(0)
