import cv2.cv2 as cv2
import os
import json
import numpy as np


def get_seats(reserved_number, empty_number):  # 获取预约位置的坐标信息
    with open('seats_test.json', 'r') as f:
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
    yy2 = np.min([ymax1, ymax2])

    aera1 = (xmax1 - xmin1 + 1) * (ymax1 - ymin1 + 1)
    aera2 = (xmax2 - xmin2 + 1) * (ymax2 - ymin2 + 1)

    inter_aera = (np.max([0, xx2 - xx1])) * (np.max([0, yy2 - yy1]))
    # iou = inter_aera / (aera1 + aera2 - inter_aera + 1e-6)
    fake_iou = inter_aera / (aera1 + 1e-6)
    return fake_iou


def is_center(bbox1, bbox2):
    if bbox1[0] >= bbox2[0] and bbox1[1] >= bbox2[1] and bbox1[2] <= bbox2[2] and bbox1[3] <= bbox2[3]:
        return True
    return False


def update_seats(n, h, w, head_location, number, the_dict):
    print(n, h, w, head_location, number)

    if number in the_dict.keys():
        if len(the_dict[number])<n:
            the_dict[number].insert(0, head_location)
        else:
            the_dict[number].insert(0, head_location)
            the_dict[number].pop()
            update(number, the_dict[number], h, w)
    else:
        the_dict.update({number:[head_location]})
    return the_dict


def update(number, head_locations, height, width):
    print(number, head_locations, height, width)
    with open('seats_test.json', 'r') as f:
        content = f.read()
        all_seats = json.loads(content)
    minx, miny, maxx, maxy = width, height, 0, 0
    for i in range(len(head_locations)):
        y = height * (float(head_locations[i][1]))
        x = width * (float(head_locations[i][0]))
        h = height * (float(head_locations[i][3]))
        w = width * (float(head_locations[i][2]))
        ymin = int(y - h / 2)
        xmin = int(x - w / 2)
        ymax = int(y + h / 2)
        xmax = int(x + w / 2)
        if ymin < miny: miny = ymin
        if xmin < minx: minx = xmin
        if ymax > maxy: maxy = ymax
        if xmax > maxx: maxx = xmax
    x = width * (float(all_seats[str(number)]['x']))
    y = height * (float(all_seats[str(number)]['y']))
    h = height * (float(all_seats[str(number)]['height']))
    w = width * (float(all_seats[str(number)]['width']))
    ymin = int(y - h / 2)
    xmin = int(x - w / 2)
    ymax = int(y + h / 2)
    xmax = int(x + w / 2)
    x1 = (xmin + minx) / 2.0
    y1 = (ymin + miny) / 2.0
    x2 = (xmax + maxx) / 2.0
    y2 = (ymax + maxy) / 2.0
    w = x2 - x1
    h = y2 - y1
    center_x = (x1 + w/2)/width
    center_y = (y1 + h/2)/height
    w = w/width
    h = h/height
    all_seats[str(number)]['x'] = str(center_x)
    all_seats[str(number)]['y'] = str(center_y)
    all_seats[str(number)]['width'] = str(w)
    all_seats[str(number)]['height'] = str(h)
    the_dict = json.dumps(all_seats)
    with open('seats_test.json', 'w') as f:
        f.write(the_dict)


def detect(img_path, reserved_seats, empty_seats):

    f = open('buffer.json', 'r')
    content = f.read()
    if content == '':
        the_dict = {}
    else:
        the_dict = json.loads(content)
    f.close()
    reserved_locations, empty_locations = get_seats(reserved_seats, empty_seats)  # 读取json,获取座位列表
    os.system("python detect.py --save-txt  --exist-ok --hide-labels --source {}".format(img_path))  # 进行检测，得到检测结果
    img_name = os.path.basename(img_path)  # 图片名
    detected_img_path = 'runs/detect/exp/{}'.format(img_name)  # 检测结果图片路径
    detected_img = cv2.imread(detected_img_path)  # 读取图片
    size = detected_img.shape
    h = size[0]
    w = size[1]
    background = np.zeros([h, w, 3], np.uint8)
    img_name_pre = img_name.split('.')[0]
    head_txt_path = 'runs/detect/exp/labels/{}.txt'.format(img_name_pre)  # 检测结果坐标路径
    head_array = []
    head_count = 0
    with open(head_txt_path) as file:  # 打开检测结果坐标路径
        for line in file:
            str_list = line.split()
            head_array.append(str_list)
            head_count += 1
    head_center_locations = get_coordinate(h, w, head_array, 0.55)  # 获取人头中心坐标
    head_locations = get_coordinate(h, w, head_array, 1.0)  # 获取人头坐标
    reserved_locations = get_coordinate(h, w, reserved_locations, 1.0)  # 获取预约座位坐标
    empty_locations = get_coordinate(h, w, empty_locations, 1.0)  # 获取空置座位坐标
    empty_seats_number = []  # 预约但无人座位号
    occupied_seats_number = []  # 有人但无预约座位号



    # 对每个预约座位进行遍历，如果无人就画框并记录座位号
    for i in range(len(reserved_locations)):
        max_iou = 0.0
        head_number = 0
        found = False
        for j in range(len(head_locations)):
            iou = cal_iou(head_locations[j][1:5], reserved_locations[i][1:5])
            # print(iou, head_locations[j][1:5], reserved_locations[i][1:5])
            if iou > max_iou and iou > 0.6:
                found = True
                max_iou = iou
                head_number = j
        # print(max_iou)
        have_head = is_center(head_center_locations[head_number][1:5], reserved_locations[i][1:5])

        if found and have_head:
            the_dict = update_seats(20, h, w, head_array[head_number][1:5], reserved_locations[i][0], the_dict)
            # cv2.rectangle(background, (reserved_locations[i][1], reserved_locations[i][2]),
            #               (reserved_locations[i][3], reserved_locations[i][4]), (0, 0, 255), 1)  # 自适应后的框
            # cv2.rectangle(background, (reserved_locations[i][1], reserved_locations[i][2]),
            #               (reserved_locations[i][3], reserved_locations[i][4]), (0, 255, 0), 1)  # 自适应前的框


        if not have_head and not found:
            cv2.rectangle(detected_img, (reserved_locations[i][1], reserved_locations[i][2]),
                          (reserved_locations[i][3], reserved_locations[i][4]), (0, 255, 0), 1)
            text = reserved_locations[i][0]
            empty_seats_number.append(text)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(detected_img, text, (reserved_locations[i][1], reserved_locations[i][2]),
                        font, 0.4, (0, 0, 255), 1)

    # 对每个空置座位框进行遍历，如果有人就画框并记录座位号

    for i in range(len(empty_locations)):
        max_iou = 0.0
        head_number = 0
        found = False
        for j in range(len(head_center_locations)):
            iou = cal_iou(head_locations[j][1:5], empty_locations[i][1:5])
            if iou > max_iou and iou > 0.6:
                found = True
                max_iou = iou
                head_number = j
        have_head = is_center(head_center_locations[head_number][1:5], empty_locations[i][1:5])
        if have_head and found:
            the_dict = update_seats(20, h, w, head_array[head_number][1:5], empty_locations[i][0], the_dict)
            cv2.rectangle(detected_img, (empty_locations[i][1], empty_locations[i][2]),
                          (empty_locations[i][3], empty_locations[i][4]), (205, 0, 0), 1)
            text = empty_locations[i][0]
            occupied_seats_number.append(text)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(detected_img, text, (empty_locations[i][1], empty_locations[i][2]), font, 0.4, (0, 0, 255), 1)

    the_dict = json.dumps(the_dict)
    f = open("buffer.json", 'w+')
    f.write(the_dict)
    f.close()
    if os.path.exists(head_txt_path):
        os.remove(head_txt_path)

    # with open('seats.json', 'r') as f:
    #     content = f.read()
    #     before_seats = json.loads(content)
    # with open('seats_test.json', 'r') as f:
    #     content = f.read()
    #     after_seats = json.loads(content)
    # before_array = []
    # after_array = []
    # for i in range(100, 500):
    #     if str(i) in before_seats.keys():
    #         seat = before_seats[str(i)]
    #         before_array.append(str(i), seat['x'], seat['y'], seat['width'], seat['height'])
    #     if str(i) in after_seats.keys():
    #         seat = after_seats[str(i)]
    #         after_array.append(str(i), seat['x'], seat['y'], seat['width'], seat['height'])


    # cv2.imshow("iamge", background)
    # cv2.waitKey(0)

    return detected_img, empty_seats_number, occupied_seats_number, head_count


if __name__ == '__main__':
    for i in range(1,57):
        img = 'pictures/{}.jpg'.format(i)
        reserved_seat = list(range(100, 500))
        empty_seat = []
        detected, empty_numbers, occupied_numbers, counts = detect(img, reserved_seat, empty_seat)  # 检测


    # cv2.imwrite('data/result/result.jpg', detected)
    # cv2.imshow('result', detected)
    # cv2.waitKey(0)
