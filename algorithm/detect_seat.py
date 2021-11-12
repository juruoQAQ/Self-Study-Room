import cv2.cv2 as cv2
import os
import json

all_seats = {}


def get_reserved_seat(seats):  # 获取预约位置的坐标信息
    seats_location = []
    for i in range(len(seats)):
        if str(seats[i]) in all_seats.keys():
            seat = all_seats[str(seats[i])]
            seats_location.append([str(seats[i]), seat['x'], seat['y'], seat['width'], seat['height']])

    return seats_location


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


def detect(location):
    os.system("python ../detect.py --save-txt --classes 1 --exist-ok --hide-labels")
    img_path = '../runs/detect/exp/studyroom.png'
    img = cv2.imread(img_path)
    size = img.shape
    h = size[0]
    w = size[1]
    head_txt_path = '../runs/detect/exp/labels/studyroom.txt'
    head_array = []
    with open(head_txt_path) as file:
        for line in file:
            str_list = line.split()
            head_array.append(str_list)
    head_array = get_coordinate(h, w, head_array, 0.75)
    location = get_coordinate(h, w, location, 1.0)

    for i in range(len(location)):
        head_miss = True
        for j in range(len(head_array)):
            if (head_array[j][1] >= location[i][1] and head_array[j][2] >= location[i][2]
                    and head_array[j][3] <= location[i][3] and head_array[j][4] <= location[i][4]):
                head_miss = False
                break
        # cv2.rectangle(img, (location[i][1], location[i][2]), (location[i][3], location[i][4]), (0, 255, 0), 1)
        # text = location[i][0]
        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(img, text, (location[i][1], location[i][2]), font, 0.3, (0, 0, 255), 1)
        if head_miss:
            cv2.rectangle(img, (location[i][1], location[i][2]), (location[i][3], location[i][4]), (0, 255, 0), 1)
            text = location[i][0]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, text, (location[i][1], location[i][2]), font, 0.3, (0, 0, 255), 1)

    cv2.imshow("test", img)
    cv2.waitKey(0)


if __name__ == '__main__':
    with open('seats.json', 'r') as f:
        content = f.read()
        all_seats = json.loads(content)
    reserved_seats = list(range(1, 500))
    locations = get_reserved_seat(reserved_seats)  # 获取预约位置的坐标信息
    detect(locations)  # 检测
