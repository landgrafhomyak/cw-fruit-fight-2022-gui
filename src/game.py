import re

from PySide2.QtCore import QByteArray, QRect, Qt
from PySide2.QtGui import QColor, QPen
from PySide2.QtSvg import QSvgRenderer
from res import svg_apple, svg_banana, svg_cherry, svg_lemon, svg_orange, svg_pineapple, svg_watermelon


class Fruit:
    __slots__ = ("__svg_renderer", "__emoji")

    @property
    def svg_renderer(self):
        return self.__svg_renderer

    @property
    def emoji(self):
        return self.__emoji

    def __init__(self, emoji, svg_source):
        data = QByteArray(svg_source.encode("utf-8"))
        self.__emoji = emoji
        self.__svg_renderer = QSvgRenderer(data)

    @staticmethod
    def emoji2enum(emoji):
        for entry in Fruit.Apple, Fruit.Banana, Fruit.Cherry, Fruit.Lemon, Fruit.Orange, Fruit.Pineapple, Fruit.Watermelon:
            if entry.emoji == emoji:
                return entry
        else:
            raise ValueError("Unknown emoji")


Fruit.Apple = Fruit("\U0001F34F", svg_apple)
Fruit.Banana = Fruit("\U0001F34C", svg_banana)
Fruit.Cherry = Fruit("\U0001f352", svg_cherry)
Fruit.Lemon = Fruit("\U0001F34B", svg_lemon)
Fruit.Orange = Fruit("\U0001F34A\uFE0F", svg_orange)
Fruit.Pineapple = Fruit("\U0001F34D\uFE0F", svg_pineapple)
Fruit.Watermelon = Fruit("\U0001F349", svg_watermelon)


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
        qp.setPen(QPen(QColor(0, 0, 0)))
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(x, y, height * 2, height)
        self.__left.svg_renderer.render(qp, QRect(x + 2, y + 2, height - 4, height - 3))
        self.__right.svg_renderer.render(qp, QRect(x + height + 2, y + 2, height - 4, height - 3))


_pattern_1 = re.compile(r"^Fruit war (ongoing|ended)!\nStamina:\s*(-?\d+)\U0001F50B\n([\s\S]+)\n---\n([^\n]+)\n---")
_pattern_2 = re.compile(r"(?<=\n)(\U0001F7E2|\u26AA\uFE0F)([^\n]+)\n([^\n]+)(?=\n)")
_pattern_3 = re.compile(r"\[([^\]]+)\]")
_pattern_4 = re.compile("|".join(map(lambda f: f.emoji, (Fruit.Apple, Fruit.Banana, Fruit.Cherry, Fruit.Lemon, Fruit.Orange, Fruit.Pineapple, Fruit.Watermelon))))


class GameState:
    __slots__ = ("__is_ended", "__stamina", "__players", "__table")

    def __new__(cls, raw_text):
        m1 = _pattern_1.search(raw_text)
        if m1 is None:
            return None

        self = super().__new__(cls)
        self.__is_ended = m1.group(1) == "ended"
        self.__stamina = int(m1.group(2))

        m2s = _pattern_2.findall(m1.group(3))
        players = []
        for m2 in m2s:
            m3s = _pattern_3.findall(m2[2])
            bones = []
            for m3 in m3s:
                m4 = _pattern_4.findall(m3)
                if len(m4) != 2:
                    raise ValueError("Bone must have exactly 2 emojis")
                bones.append(Bone(Fruit.emoji2enum(m4[0]), Fruit.emoji2enum(m4[1])))
            players.append(GameState.Player(m2[0] == "\U0001F7E2", m2[1], tuple(bones)))

        self.__players = tuple(players)

        return self

    @property
    def is_ended(self):
        return self.__is_ended

    @property
    def stamina(self):
        return self.__stamina

    @property
    def players(self):
        return self.__players

    class Player:
        __slots__ = ("__is_turn", "__name", "__bones")

        def __init__(self, is_turn, name, bones):
            self.__is_turn = is_turn
            self.__name = name
            self.__bones = bones

        @property
        def is_turn(self):
            return self.__is_turn

        @property
        def name(self):
            return self.__name

        @property
        def bones(self):
            return self.__bones
