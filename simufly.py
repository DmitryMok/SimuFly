'''
Функции для эмуляции полета над подверхностью:
start_simulation - запускает симуляцию, вырезает базовый блок, в котором находимся
crop_rotated_frame - поворачивает базовый блок на угол angle и вырезает из него блок для отображения
display_crop_place - показывает в углу рамку, где находится вырезанный фрагмент
rotate_rect - преобразует координаты прямоугольнака в новые после поворота (используется в display_crop_place)
out_of_image - выводит out of signal, если вышли за пределы подложки
'''

import cv2
import math
import numpy as np

def display_crop_place(image):
    # Рисуем прямоугольник и крестик с координатами
    x_pad, y_pad = 10, 10   # отступ от края
    x1, x2, y1, y2 = block_size-x_pad-width//scale, block_size-x_pad, y_pad, y_pad+height//scale

    # Поворот координат
    points = rotate_rect(x1+int(x)//scale-block_size//(2*scale), y1+int(y)//scale-block_size//(2*scale)
                                                 , x1+int(x)//scale+block_size//(2*scale), y1+int(y)//scale+block_size//(2*scale), angle)

    cv2.rectangle(image, (x1,y1), (x2,y2), (0, 150, 0), 1)
    cv2.polylines(image, [points], True, (0, 0, 150), 1)
    return image


def crop_rotated_frame(frame, angle):
    # Поворачиваем блок на заданный угол
    M = cv2.getRotationMatrix2D((base_block/2, base_block/2), angle, 1.0)
    rotated_frame = cv2.warpAffine(frame, M, (base_block, base_block))

    # Вырезаем блок изображения размером block_size на block_size пикселей из центра повернутого блока
    x_block = base_block // 2 - block_size // 2
    y_block = base_block // 2 - block_size // 2

    return rotated_frame[y_block:y_block+block_size, x_block:x_block+block_size]

def rotate_rect(x1, y1, x2, y2, angle):
    # Находим центр прямоугольника
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    # Находим длину и ширину прямоугольника
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    # Переводим угол в радианы
    angle_rad = math.radians(angle)
    # Находим новые координаты углов прямоугольника
    x1_new = int(cx + (x1 - cx) * math.cos(angle_rad) - (y1 - cy) * math.sin(angle_rad))
    y1_new = int(cy + (x1 - cx) * math.sin(angle_rad) + (y1 - cy) * math.cos(angle_rad))
    x2_new = int(cx + (x2 - cx) * math.cos(angle_rad) - (y2 - cy) * math.sin(angle_rad))
    y2_new = int(cy + (x2 - cx) * math.sin(angle_rad) + (y2 - cy) * math.cos(angle_rad))
    x3_new = int(cx + (x2 - cx) * math.cos(angle_rad) - (y1 - cy) * math.sin(angle_rad))
    y3_new = int(cy + (x2 - cx) * math.sin(angle_rad) + (y1 - cy) * math.cos(angle_rad))
    x4_new = int(cx + (x1 - cx) * math.cos(angle_rad) - (y2 - cy) * math.sin(angle_rad))
    y4_new = int(cy + (x1 - cx) * math.sin(angle_rad) + (y2 - cy) * math.cos(angle_rad))
    # Возвращаем новые координаты прямоугольника
    return np.array([[x1_new, y1_new], [x4_new, y4_new], [x2_new, y2_new], [x3_new, y3_new]])

# функция используется при выходе за пределы изображения
def out_of_image():
    # Задаем размеры изображения
    image = np.zeros((block_size, block_size, 3), np.uint8) + 50

    # Задаем текст для вывода
    text = "Signal lost!"

    # Задаем координаты и размеры шрифта
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    thickness = 2

    # Задаем цвет текста и его толщину
    color = (0, 0, 255)

    # Определяем размеры текста
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

    # Определяем координаты, где будет располагаться начало текста
    text_x = int((image.shape[1] - text_size[0]) / 2)  # центровка по горизонтали
    text_y = int((image.shape[0] + text_size[1]) / 2)  # центровка по вертикали

    # Выводим текст на изображение
    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness)

    return image


def start_simulation(landscape_file, bl_size = 640, ang = None, x_coord = None, y_coord = None):
    global image, x, y, angle, height, width, block_size, base_block, scale, speed

    x, y, angle = x_coord, y_coord, ang
    block_size = bl_size    # размер вырезаемого блока
    base_block = int((block_size ** 2 / 2) ** 0.5) * 2  # рамка, которую повернем и вырежем блок
    speed = 10      # смещение при движении фрагмента
    speed_ang = 5   # скорость поворота
    scale = 100  # уменьшение размера для отображения, где вырезан текущий фрагмент

    # Загружаем изображение
    image = cv2.imread(landscape_file)
    height, width, _ = image.shape
    if not x or not y:
        x, y = width // 2, height // 2

    if not angle:
        angle = 0  # угол поворота

    print(image.shape)
    while True:
        # Вырезаем базовый блок для поворота (чтобы не поворачивать всю подложку)
        cropped_image_base = image[int(y) - base_block // 2:int(y) + base_block // 2,
                             int(x) - base_block // 2:int(x) + base_block // 2, :]
        # используем размер вырезанного кадра для определения не вышли ли за изображение
        if cropped_image_base.shape[0] and cropped_image_base.shape[1]:
            cropped_image = crop_rotated_frame(cropped_image_base, angle)
        else:
            cropped_image = out_of_image()
        # print(cropped_image.shape)

        # Преобразование угла из градусов в радианы
        angle_rad = math.radians(angle + 90)

        # отображаем место на изображении
        cropped_image = display_crop_place(cropped_image.copy())

        # Сохраняем вырезанную область в новый файл
        cv2.imshow('SimuFly: UAV Flight Simulator', cropped_image)
        # Ожидаем нажатия клавиш
        key = cv2.waitKey(0)

        # Если нажата клавиша "q", выходим из цикла
        if key == ord('q'):
            break

        # Вычисление приращения координат
        dx = speed * math.cos(angle_rad)
        dy = speed * math.sin(angle_rad)

        # Изменяем координаты в зависимости от направления нажатой стрелки
        if key == ord('a'):  # Стрелка влево
            angle -= speed_ang
        elif key == ord('d'):  # Стрелка вправо
            angle += speed_ang
        elif key == ord('s'):  # Стрелка вниз
            x += dx
            y += dy
        elif key == ord('w'):  # Стрелка вверх
            x -= dx
            y -= dy

    cv2.destroyAllWindows()
