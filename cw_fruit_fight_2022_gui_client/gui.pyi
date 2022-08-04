from typing import Set, Tuple

from PySide2.QtCore import Signal
from PySide2.QtGui import QCloseEvent, QMouseEvent, QPaintEvent, QResizeEvent
from PySide2.QtWidgets import QMainWindow, QWidget

from .client import Cwff2022gcClientThread
from .game import Cwff2022gcBone, Cwff2022gcChatInfo, Cwff202gcSkipTurnButton


class Cwff2022gcAuthConfiguration(QWidget):
    send_phone = Signal(str)
    send_code_and_password = Signal(str, str, str)

    def __init__(self, parent: QWidget, auth_factory: Cwff2022gcClientThread) -> None: ...


class Cwff2022gcBonesRow(QWidget):
    clicked = Signal(object)

    def __init__(self, parent: QWidget) -> None: ...

    def resizeEvent(self, event: QResizeEvent) -> None: ...

    def set_data(self, data: Tuple[Cwff2022gcBone, ...]) -> None: ...

    def paintEvent(self, event: QPaintEvent) -> None: ...

    def mousePressEvent(self, event: QMouseEvent) -> None: ...


class Cwff2022gcChatsList(QWidget):
    selected = Signal(object)
    unselected = Signal()

    def __init__(self, parent: QWidget) -> None: ...

    def move_cid_to_top(self, cid: int) -> None: ...

    def remove_cid(self, cid: int) -> None: ...

    def ensure_chat(self, chat: Cwff2022gcChatInfo) -> None: ...

    def set_turn_for_chats(self, cids: Set[int]) -> None: ...


class Cwff2022gcClientConfiguration(QWidget):
    create_client_in_memory = Signal(str, str)
    create_client_with_file = Signal(str, str, str)

    def __init__(self, parent: QWidget, client_factory: Cwff2022gcClientThread) -> None: ...


class Cwff2022gcGameConfigPanel(QWidget):
    set_ingame_name = Signal(str)

    def __init__(self, parent: QWidget) -> None: ...


class Cwff2022gcStaminaHBar(QWidget):
    def __init__(self, parent: QWidget) -> None: ...

    def paintEvent(self, event: QPaintEvent) -> None: ...

    def set_left_max(self, left: int, mx: int) -> None: ...

    def set_left(self, left: int) -> None: ...


class Cwff2022gcStaminaPanel(QWidget):
    def __init__(self, parent: QWidget) -> None: ...

    def set_left_max(self, left: int, mx: int) -> None: ...

    def set_left(self, left: int) -> None: ...


class Cwff2022gcTurnIndicator(QWidget):
    def __init__(self, parent: QWidget) -> None: ...

    def heightForWidth(self, width: int) -> int: ...

    def resizeEvent(self, event: QResizeEvent) -> None: ...

    def set(self, value: bool) -> None: ...

    def paintEvent(self, event: QPaintEvent) -> None: ...


class Cwff2022gcPlayersHands(QWidget):
    def __init__(self, parent: QWidget) -> None: ...

    def set_row(self, index: int, turn: bool, name: str, hand: Tuple[Cwff2022gcBone, ...]) -> None: ...

    def ensure_players_count(self, count: int) -> None: ...

    def clear(self) -> None: ...


class Cwff2022gcGamePanel(QWidget):
    skip_turn = Signal(Cwff202gcSkipTurnButton)

    def __init__(self, parent: QWidget, client_worker: Cwff2022gcClientThread) -> None: ...

    def set_data(self, data: Cwff2022gcChatInfo, max_stamina: int) -> None: ...


class Cwff2022gcGameTab(QWidget):
    def __init__(self, parent: QWidget, client_worker: Cwff2022gcClientThread) -> None: ...


class Cwff2022gcMainWindow(QMainWindow):
    closed = Signal()

    def __init__(self, client_worker: Cwff2022gcClientThread) -> None: ...

    def closeEvent(self, event: QCloseEvent) -> None: ...
