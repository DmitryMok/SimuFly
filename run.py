# работа с подложкой аэроснимка для симуляции полета над поверхностью

from simufly import *   # загружаем нужные функции

# Определяем координаты стартовой точки (по умолчанию будет середина подложки) и угол поворота в градусах
x, y, ang = 1000, 1000, 0

# Определяем размер блока (по умолчанию 640)
block_size = 640

# запускаем симулятор
start_simulation('landscape.jpg', bl_size = block_size, ang = 0, x_coord = x, y_coord = y)
# start_simulation('img/original.tiff')