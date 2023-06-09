# SimuFly

Данный проект представляет собой простую программу на Python, которая позволяет симулировать полет БПЛА (беспилотного летательного аппарата) над поверхностью земли, используя фотографию поверхности земли в качестве входных данных.
В программе реализована функция вырезания фрагментов изображения в зависимости от положения БПЛА, а также управление движением кнопками w, s, a, d для движения вперед или поворота. Для выхода используйте 'q'.

<img src="/screenshot1.png" alt="интерфейс программы" width="500"/>

В случае выхода за пределы изображения, программа выводит предупреждение "signal lost" :)

<img src="/screenshot2.png" alt="интерфейс программы" width="500"/>

Данный проект может быть полезен для быстрого тестирования алгоритмов компьютерного зрения. Вместо установки Gazebo, Airsim и подобных. Для этого и создавался.

# Как использовать

```python
# загружаем модуль с функциями
from simufly import *   

# Определяем координаты стартовой точки (по умолчанию будет середина подложки) и угол поворота в градусах
x, y, ang = 1000, 1000, 0

# Определяем размер блока (по умолчанию 640)
block_size = 640

# запускаем симулятор указав файл подложки
start_simulation('landscape.jpg', bl_size = block_size, ang = 0, x_coord = x, y_coord = y)
```
# Посмотрите видео
[![посмотрите видео](https://img.youtube.com/vi/ZCHeAuflB2A/0.jpg)](https://youtu.be/ZCHeAuflB2A)


