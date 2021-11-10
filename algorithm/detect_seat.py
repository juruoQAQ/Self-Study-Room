import cv2.cv2 as cv2
import os

txt_array = []


def get_seats_location():
    txt_path = 'labels/study_room_1.txt'
    with open(txt_path) as f:
        for line in f:
            str_list = line.split()
            txt_array.append(str_list)


def get_reserved_seat(seats):  # 获取预约位置的坐标
    seats_location = []
    for i in range(len(seats)):
        seats_location.append(txt_array[seats[i]])

    return seats_location


def get_coordinate(height, width, array, para):
    coordinates = []
    para = 1.0 - para
    for i in range(len(array)):
        x = height * (float(array[i][2]))
        y = width * (float(array[i][1]))
        h = height * (float(array[i][4]))
        w = width * (float(array[i][3]))
        xvar = w*para
        yvar = h*para
        ymin = int(x - h / 2 + yvar)
        xmin = int(y - w / 2 + xvar)
        ymax = int(x + h / 2 - yvar)
        xmax = int(y + w / 2 - xvar)
        coordinates.append([xmin, ymin, xmax, ymax])
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
    with open(head_txt_path) as f:
        for line in f:
            str_list = line.split()
            head_array.append(str_list)
    head_array = get_coordinate(h, w, head_array, 0.7)
    location = get_coordinate(h, w, location, 1.0)

    for i in range(len(location)):
        head_miss = True
        for j in range(len(head_array)):
            if (head_array[j][0] >= location[i][0] and head_array[j][1] >= location[i][1]
                     and head_array[j][2] <= location[i][2] and head_array[j][3] <= location[i][3]):
                head_miss = False
                break
        if head_miss:
            cv2.rectangle(img, (location[i][0], location[i][1]), (location[i][2], location[i][3]), (0, 255, 0), 1)
            # text = '{}'.format(i)  # 座位标号未实现
            text = 'null'
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, text, (location[i][0], location[i][1]), font, 0.5, (0, 0, 255), 1)

    cv2.imshow("test", img)
    cv2.waitKey(0)


if __name__ == '__main__':
    get_seats_location()
    # reserved_seats = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58]  # 预约的座位
    reserved_seats = list(range(0, 83))
    locations = get_reserved_seat(reserved_seats)  # 获取预约座位坐标
    detect(locations)  # 检测
