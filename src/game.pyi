from typing import Optional, Tuple

from PySide2.QtGui import QPainter
from PySide2.QtSvg import QSvgRenderer


class Fruit:
    __slots__ = ...
    __svg_renderer: QSvgRenderer
    __emoji: str

    @property
    def svg_renderer(self) -> QSvgRenderer: ...

    @property
    def emoji(self) -> str: ...

    def __init__(self, emoji: str, svg_source: str) -> None: ...

    @staticmethod
    def emoji2enum(emoji: str) -> Fruit: ...

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


class GameState:
    __slots__ = ...

    __is_ended: bool
    __stamina: int
    __players: Tuple['GameState.Player', ...]
    __table: None

    def __new__(cls, raw_text: str) -> Optional[GameState]: ...

    @property
    def is_ended(self) -> bool: ...

    @property
    def stamina(self) -> int: ...

    @property
    def players(self) -> Tuple['GameState.Player', ...]: ...

    class Player:
        __slots__ = ...

        __is_turn: bool
        __name: str
        __bones: Tuple[Bone, ...]

        def __init__(self, is_turn: bool, name: str, bones: Tuple[Bone, ...]) -> None: ...

        @property
        def is_turn(self) -> bool: ...

        @property
        def name(self) -> str: ...

        @property
        def bones(self) -> Tuple[Bone, ...]: ...
