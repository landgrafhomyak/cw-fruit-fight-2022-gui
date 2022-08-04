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


_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Apple, "\U0001F34F")
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Banana, "\U0001F34C")
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Cherry, "\U0001f352")
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Lemon, "\U0001F34B")
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Orange, "\U0001F34A\uFE0F")
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Pineapple, "\U0001F34D\uFE0F")
_Cwff2022gcFruit_SetEmoji(Cwff2022gcFruit_Watermelon, "\U0001F349")

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

cdef class Cwff2022gcChatInfo:
    cdef readonly object cid
    cdef readonly str name
    cdef public bint is_turn
    cdef public int players_count

    def __cinit__(self, cid, name):
        self.cid = cid
        self.name = name
        self.is_turn = False
        self.players_count = 0

cdef class Cwff202gcButtonWithBone(Cwff2022gcBone):
    cdef readonly object button

    def __init__(self, left, right, button):
        super().__init__(left, right)
        self.button = button

cdef class Cwff202gcSkipTurnButton:
    cdef readonly object button

    def __cinit__(self, button):
        self.button = button

cdef object __pattern_1 = re.compile(r"^Fruit war (ongoing|ended)!\nStamina:\s*(-?\d+)\U0001F50B\n([\s\S]+)\n---\n([^\n]+)\n---")
cdef object __pattern_2 = re.compile(r"(?<=\n)(\U0001F7E2|\u26AA\uFE0F)([^\n]+)\n([^\n]+)(?=\n)")
cdef object __pattern_3 = re.compile(r"\[([^\]]+)\]")

cdef extern from *:
    """
    #define set_to_pointer(PTR, VALUE) (Py_INCREF(VALUE), *(PTR) = (VALUE))
    """
    void set_to_pointer(PyObject ** PTR, object VALUE)

cdef public int _Cwff2022gcGameState_New(
        str raw_text,
        object buttons_in,
        int *is_ended,
        PyObject ** stamina,
        PyObject ** players,
        PyObject ** table,
        PyObject ** buttons_out
) except -1:
    m1 = __pattern_1.search(raw_text)
    if m1 is None:
        return 0

    is_ended[0] = 1 if m1.group(1) == "ended" or buttons_in is None else 0
    set_to_pointer(stamina, int(m1.group(2)))

    m2s = __pattern_2.findall(m1.group(3))
    players_r = []
    for m2 in m2s:
        m3s = __pattern_3.findall(m2[2])
        bones = []
        for m3 in m3s:
            m4 = Cwff2022gcFruit.emoji_regexp.findall(m3)
            if len(m4) != 2:
                raise ValueError("Bone must have exactly 2 emojis")
            bones.append(Cwff2022gcBone(Cwff2022gcFruit.from_emoji(m4[0]), Cwff2022gcFruit.from_emoji(m4[1])))
        players_r.append(Cwff2022gcPlayer(m2[0] == "\U0001F7E2", m2[1], tuple(bones)))

    set_to_pointer(players, tuple(players_r))

    t = Cwff2022gcFruit.emoji_regexp.findall(m1.group(4))
    if len(t) < 2:
        raise ValueError("Invalid game table")

    set_to_pointer(table, Cwff2022gcBone(Cwff2022gcFruit.from_emoji(t[0]), Cwff2022gcFruit.from_emoji(t[-1])))

    if not is_ended[0]:
        p_buttons = []
        for row in buttons_in:
            for btn in row:
                if "Accept Fate" in btn.text:
                    set_to_pointer(buttons_out, Cwff202gcSkipTurnButton(btn))
                    break
                m4 = Cwff2022gcFruit.emoji_regexp.findall(btn.text)
                if len(m4) != 2:
                    raise ValueError("Button with bone must have exactly 2 emojis")
                p_buttons.append(Cwff202gcButtonWithBone(Cwff2022gcFruit.from_emoji(m4[0]), Cwff2022gcFruit.from_emoji(m4[1]), btn))
            else:
                continue
            break
        else:
            set_to_pointer(buttons_out, tuple(p_buttons))
    else:
        buttons_out[0] = NULL

    return 1

cdef extern:
    type _Cwff2022gcGameState_PrepareType(object dct)

Cwff2022gcGameState = _Cwff2022gcGameState_PrepareType(dict())

cdef class Cwff2022gcPlayer:
    cdef readonly bint is_turn
    cdef readonly str name
    cdef readonly tuple bones

    def __cinit__(self, bint is_turn, str name, tuple bones):
        self.is_turn = is_turn
        self.name = name
        self.bones = bones
