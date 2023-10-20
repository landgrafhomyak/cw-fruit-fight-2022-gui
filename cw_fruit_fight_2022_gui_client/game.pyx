import re

import pkg_resources

from cpython.object cimport PyObject

from PySide2.QtCore import QRect, QByteArray
from PySide2.QtGui import QColor, QPen, Qt
from PySide2.QtSvg import QSvgRenderer


cdef extern:
    PyObject *Cwff2022gcFruit_Apple
    PyObject *Cwff2022gcFruit_Banana
    PyObject *Cwff2022gcFruit_Cherry
    PyObject *Cwff2022gcFruit_Lemon
    PyObject *Cwff2022gcFruit_Orange
    PyObject *Cwff2022gcFruit_Pineapple
    PyObject *Cwff2022gcFruit_Watermelon

    void _Cwff2022gcFruit_SetEmoji(PyObject *self, object value)
    str _Cwff2022gcFruit_GetEmoji(object self)
    void _Cwff2022gcFruit_SetRenderer(PyObject *self, object value)
    type _Cwff2022gcFruit_PrepareType(object dct)


_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Apple, "\U0001F383") # pumpkin
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Banana, "\U0001fac0") # heart
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Cherry, "\U0001f9e0") # brain
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Lemon, "\U0001fa78") # blood
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Orange, "\U0001f9b4") # bone
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Pineapple, "\U0001f480") # skull
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Watermelon, "\U0001f9b7") # tooth

_Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Apple, QSvgRenderer(QByteArray(pkg_resources.resource_string(__name__, "./apple.svg"))))
_Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Banana, QSvgRenderer(QByteArray(pkg_resources.resource_string(__name__, "./banana.svg"))))
_Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Cherry, QSvgRenderer(QByteArray(pkg_resources.resource_string(__name__, "./cherry.svg"))))
_Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Lemon, QSvgRenderer(QByteArray(pkg_resources.resource_string(__name__, "./lemon.svg"))))
_Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Orange, QSvgRenderer(QByteArray(pkg_resources.resource_string(__name__, "./orange.svg"))))
_Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Pineapple, QSvgRenderer(QByteArray(pkg_resources.resource_string(__name__, "./pineapple.svg"))))
_Cwff2022gcFruit_SetRenderer(Cwff2022gcFruit_Watermelon, QSvgRenderer(QByteArray(pkg_resources.resource_string(__name__, "./watermelon.svg"))))

cpdef __Cwff2022gcFruit_FromEmoji(emoji):
    for entry in Cwff2022gcFruit.__values__:
        if entry.emoji == emoji:
            return entry
    else:
        raise ValueError("Unknown emoji")

__Cwff2022gcFruit_Values = (<object> Cwff2022gcFruit_Apple, <object> Cwff2022gcFruit_Banana, <object> Cwff2022gcFruit_Cherry, <object> Cwff2022gcFruit_Lemon, <object> Cwff2022gcFruit_Orange, <object> Cwff2022gcFruit_Pineapple, <object> Cwff2022gcFruit_Watermelon)

Cwff2022gcFruit = _Cwff2022gcFruit_PrepareType({
    "Apple": <object> Cwff2022gcFruit_Apple,
    "Banana": <object> Cwff2022gcFruit_Banana,
    "Cherry": <object> Cwff2022gcFruit_Cherry,
    "Lemon": <object> Cwff2022gcFruit_Lemon,
    "Orange": <object> Cwff2022gcFruit_Orange,
    "Pineapple": <object> Cwff2022gcFruit_Pineapple,
    "Watermelon": <object> Cwff2022gcFruit_Watermelon,
    "from_emoji": __Cwff2022gcFruit_FromEmoji,
    "__values__": __Cwff2022gcFruit_Values,
    "emoji_regexp": re.compile("|".join(map(lambda f: _Cwff2022gcFruit_GetEmoji(f), __Cwff2022gcFruit_Values)))
})

del __Cwff2022gcFruit_FromEmoji, __Cwff2022gcFruit_Values

cdef class Cwff2022gcBone:
    cdef readonly object left
    cdef readonly object right

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @staticmethod
    def height_to_width(height):
        return height * 2

    cpdef paint(self, qp, x, y, height):
        qp.setPen(QPen(QColor(0, 0, 0)))
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(x, y, height * 2, height)
        self.left.renderer.render(qp, QRect(x + 2, y + 2, height - 4, height - 3))
        self.right.renderer.render(qp, QRect(x + height + 2, y + 2, height - 4, height - 3))

cdef class Cwff202gcButtonWithBone(Cwff2022gcBone):
    cdef readonly object button

    def __init__(self, left, right, button):
        super().__init__(left, right)
        self.button = button

cdef class Cwff202gcSkipTurnButton:
    cdef readonly object button

    def __cinit__(self, button):
        self.button = button

cdef class Cwff2022gcChatInfo:
    cdef readonly object cid
    cdef readonly str name
    cdef public bint is_turn
    cdef public bint is_joinable
    cdef public bint is_started
    cdef public int players_count

    def __cinit__(self, cid, name):
        self.cid = cid
        self.name = name
        self.is_turn = False
        self.is_joinable = False
        self.is_started = False
        self.players_count = 0

cdef object __pattern_c1 = re.compile(r"^Ready to embark on \U0001F95DFruit wars:((?:\n-\s[^\n]+)*)")
cdef object __pattern_c2 = re.compile(r"(?<=\n)-\s([^\n]+)")
cdef object __pattern_g1 = re.compile(r"^Fruit war (ongoing|ended)!\nStamina:\s*(-?\d+)\U0001F50B\n([\s\S]+)\n---\n([^\n]+)\n---")
cdef object __pattern_g2 = re.compile(r"(?<=\n)(\U0001F7E2|\u26AA\uFE0F)([^\n]+)\n([^\n]+)(?=\n)")
cdef object __pattern_g3 = re.compile(r"\[([^\]]+)\]")

cdef extern:
    type _Cwff2022gcGameState_PrepareType(object dct)

cdef class Cwff2022gcCollectingGame:
    cdef readonly tuple players
    cdef readonly object join_button
    cdef readonly object start_button

    def __cinit__(self, tuple players, object join_button, object start_button):
        self.players = players
        self.join_button = join_button
        self.start_button = start_button

cdef class Cwff2022gcGameState:
    cdef readonly bint is_ended
    cdef readonly object stamina
    cdef readonly tuple players
    cdef readonly Cwff2022gcBone table
    cdef readonly object buttons

    def __cinit__(self, bint is_ended, object stamina, tuple players, Cwff2022gcBone table, object buttons):
        self.is_ended = is_ended
        self.stamina = stamina
        self.players = players
        self.table = table
        self.buttons = buttons

cdef class Cwff2022gcPlayer:
    cdef readonly bint is_turn
    cdef readonly str name
    cdef readonly tuple bones

    def __cinit__(self, bint is_turn, str name, tuple bones):
        self.is_turn = is_turn
        self.name = name
        self.bones = bones

cpdef object cwff2022gcParseGameMessage(str raw_text, object ibuttons):
    cdef object c1 = __pattern_c1.search(raw_text)
    cdef object join_button = None
    cdef object start_button = None

    if c1 is not None:
        if ibuttons is not None:
            for row in ibuttons:
                for button in row:
                    if join_button is None and "Join" in button.text:
                        join_button = button
                    if start_button is None and "Commence" in button.text:
                        start_button = button
        if start_button is None:
            raise ValueError("Start button not found")
        return Cwff2022gcCollectingGame(tuple(__pattern_c2.findall(c1.group(1))), join_button, start_button)

    cdef object m1 = __pattern_g1.search(raw_text)
    if m1 is None:
        return None

    cdef list players = []
    cdef list bones
    for m2 in __pattern_g2.findall(m1.group(3)):
        bones = []
        for m3 in __pattern_g3.findall(m2[2]):
            m4 = Cwff2022gcFruit.emoji_regexp.findall(m3)
            if len(m4) != 2:
                raise ValueError("Bone must have exactly 2 emojis")
            bones.append(Cwff2022gcBone(Cwff2022gcFruit.from_emoji(m4[0]), Cwff2022gcFruit.from_emoji(m4[1])))
        players.append(Cwff2022gcPlayer(m2[0] == "\U0001F7E2", m2[1], tuple(bones)))

    t = Cwff2022gcFruit.emoji_regexp.findall(m1.group(4))
    if len(t) < 2:
        raise ValueError("Invalid game table")

    cdef object buttons = None
    cdef list l_buttons = []
    if ibuttons is not None:
        for row in ibuttons:
            for button in row:
                if "Accept Fate" in button.text:
                    buttons = Cwff202gcSkipTurnButton(button)
                    break
                m4 = Cwff2022gcFruit.emoji_regexp.findall(button.text)
                if len(m4) != 2:
                    raise ValueError("Button with bone must have exactly 2 emojis")
                l_buttons.append(Cwff202gcButtonWithBone(Cwff2022gcFruit.from_emoji(m4[0]), Cwff2022gcFruit.from_emoji(m4[1]), button))
            else:
                continue
            break
        else:
            buttons = l_buttons

    return Cwff2022gcGameState(
        m1.group(1) == "ended" or ibuttons is None,
        int(m1.group(2)),
        tuple(players),
        Cwff2022gcBone(Cwff2022gcFruit.from_emoji(t[0]), Cwff2022gcFruit.from_emoji(t[-1])),
        buttons
    )
