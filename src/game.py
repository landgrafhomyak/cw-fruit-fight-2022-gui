from PySide6.QtCore import QByteArray, QRect, Qt
from PySide6.QtGui import QPen
from PySide6.QtSvg import QSvgRenderer
from res import *


class Fruit:
    __slots__ = ("__svg_renderer",)

    @property
    def svg_renderer(self):
        return self.__svg_renderer

    def __init__(self, svg_source):
        data = QByteArray(svg_source.encode("utf-8"))
        self.__svg_renderer = QSvgRenderer(data)


Fruit.Apple = Fruit(svg_apple)
Fruit.Banana = Fruit(svg_banana)
Fruit.Cherry = Fruit(svg_cherry)
Fruit.Lemon = Fruit(svg_lemon)
Fruit.Orange = Fruit(svg_orange)
Fruit.Pineapple = Fruit(svg_pineapple)
Fruit.Watermelon = Fruit(svg_watermelon)


class Bone:
    __slots__ = ("__left", "__right")

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    def __init__(self, left, right):
        self.__left = left
        self.__right = right

    @staticmethod
    def width(height):
        return height * 2

    def paint(self, qp, x, y, height):
        qp.setPen(QPen(Qt.Black))
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(x, y, height, height * 2)
        self.__left.svg_renderer.render(qp, QRect(2, 2, height - 4, height - 3))
        self.__right.svg_renderer.render(qp, QRect(height + 2, 2, height - 4, height - 3))
