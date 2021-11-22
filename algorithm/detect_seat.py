import cv2.cv2 as cv2
import os
import json


def get_reserved_seat(seats):  # 获取预约位置的坐标信息
    with open('seats.json', 'r') as f:
        content = f.read()
        all_seats = json.loads(content)
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


def detect(img_path, reserved_seats):
    locations = get_reserved_seat(reserved_seats)
    os.system("python detect.py --save-txt  --exist-ok --hide-labels --source {}".format(img_path))
    img_name = os.path.basename(img_path)
    detected_img_path = 'runs/detect/exp/{}'.format(img_name)
    detected_img = cv2.imread(detected_img_path)
    size = detected_img.shape
    h = size[0]
    w = size[1]
    img_name_pre = img_name.split('.')[0]
    head_txt_path = 'runs/detect/exp/labels/{}.txt'.format(img_name_pre)
    head_array = []
    with open(head_txt_path) as file:
        for line in file:
            str_list = line.split()
            head_array.append(str_list)
    head_array = get_coordinate(h, w, head_array, 0.75)
    locations = get_coordinate(h, w, locations, 1.0)

    seats_number = []
    for i in range(len(locations)):
        head_miss = True
        for j in range(len(head_array)):
            if (head_array[j][1] >= locations[i][1] and head_array[j][2] >= locations[i][2]
                    and head_array[j][3] <= locations[i][3] and head_array[j][4] <= locations[i][4]):
                head_miss = False
                break

        if head_miss:
            cv2.rectangle(detected_img, (locations[i][1], locations[i][2]), (locations[i][3], locations[i][4]), (0, 255, 0), 1)
            text = locations[i][0]
            seats_number.append(text)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(detected_img, text, (locations[i][1], locations[i][2]), font, 0.3, (0, 0, 255), 1)

    return detected_img, seats_number


if __name__ == '__main__':
    img = 'data/images/studyroom.png'
    reserved_seat = list(range(1, 500))
    detected, numbers = detect(img, reserved_seat)  # 检测
    print(numbers)
    cv2.imshow("test", detected)
    cv2.waitKey(0)

