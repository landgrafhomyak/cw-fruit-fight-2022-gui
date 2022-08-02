from PySide6.QtGui import QPainter
from PySide6.QtSvg import QSvgRenderer


class Fruit:
    __slots__ = ...
    __svg_renderer: QSvgRenderer

    @property
    def svg_renderer(self) -> QSvgRenderer: ...

    def __init__(self, svg_source: str) -> None: ...

    Apple: Fruit
    Banana: Fruit
    Cherry: Fruit
    Lemon: Fruit
    Orange: Fruit
    Pineapple: Fruit
    Watermelon: Fruit


class Bone:
    __slots__ = ...
    __left: Fruit
    __right: Fruit

    @property
    def left(self) -> Fruit: ...

    @property
    def right(self) -> Fruit: ...

    def __init__(self, left: Fruit, right: Fruit) -> None: ...

    @staticmethod
    def width(height: int) -> int: ...

    def paint(self, qp: QPainter, x: int, y: int, height: int) -> None: ...
