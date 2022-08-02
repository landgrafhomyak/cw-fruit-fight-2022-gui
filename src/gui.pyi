from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QMouseEvent, QPainter, QPaintEvent, QResizeEvent, QWheelEvent
from PySide6.QtWidgets import QButtonGroup, QGridLayout, QLabel, QLineEdit, QListView, QMainWindow, QPushButton, QRadioButton, QScrollArea, QScrollBar, QToolButton, QWidget

from game import Bone, GameState
from src.client import ClientWorker


class FruitFight2022MainWindow(QMainWindow):
    closed = Signal()

    __client_worker: ClientWorker
    __client_config_tab: FruitFight2022ClientConfiguration
    __account_auth_tab: FruitFight2022AccountAuth
    __game_interface_tab: FruitFight2022GameInterface

    def __init__(self, client_worker: ClientWorker) -> None: ...

    @Slot
    def __on_client_created(self) -> None: ...

    @Slot()
    def re_create_client(self) -> None: ...

    @Slot
    def __on_auth_completed(self) -> None: ...


class FruitFight2022ClientConfiguration(QWidget):
    __api_id_label: QLabel
    __api_id_input: QLineEdit
    __api_hash_label: QLabel
    __api_hash_input: QLineEdit
    __rb_group: QButtonGroup
    __rb_inmemory: QRadioButton
    __rb_file: QRadioButton
    __file_label: QLabel
    __file_input: QLineEdit
    __file_button: QToolButton
    __message_label: QLabel
    __create_client_button: QPushButton

    in_memory_client_creating = Signal(str, str)
    file_client_creating = Signal(str, str, str)

    def __init__(self, parent: FruitFight2022MainWindow, client_worker: ClientWorker) -> None: ...

    @Slot()
    def __create_client(self): ...

    @Slot(str)
    def __on_client_creation_fail(self, text) -> None: ...

    @Slot()
    def __inmemory_variant(self) -> None: ...

    @Slot()
    def __file_variant(self) -> None: ...


class FruitFight2022AccountAuth(QWidget):
    __phone_label: QLabel
    __phone_input: QLineEdit
    __phone_button: QPushButton
    __code_label: QLabel
    __code_input: QLineEdit
    __change_phone_button: QPushButton
    __password_label: QLabel
    __password_input: QLineEdit
    __auth: QPushButton
    __message_label: QLabel

    sending_phone = Signal(str)
    sending_code_and_password = Signal(str, str)

    def __init__(self, parent: FruitFight2022MainWindow, client_worker: ClientWorker) -> None: ...

    @Slot(str)
    def __on_send_phone_failed(self, message) -> None: ...

    @Slot(str)
    def __on_send_code_and_password_failed(self, message) -> None: ...

    @Slot()
    def __send_phone(self) -> None: ...

    @Slot()
    def __on_code_request(self) -> None: ...

    @Slot()
    def __change_phone(self) -> None: ...

    @Slot()
    def __finish_auth(self) -> None: ...

    @Slot()
    def __auth_completed(self) -> None: ...


class FruitFight2022GameInterface(QWidget):
    __chats: 'FruitFight2022GameInterface.ChatsList'
    __game: 'FruitFight2022GameInterface.GamePanel'
    __chats_data: Dict[int, GameState]
    __stamina_max_cache: Dict[int, int]
    __current_chat: Optional[int]

    def __init__(self, parent: QWidget, client_worker: ClientWorker) -> None: ...

    @Slot(object)
    def __on_chat_delete(self, cid: int) -> None: ...

    @Slot(object, str, GameState)
    def __on_chat_update(self, cid: int, data: GameState) -> None: ...

    @Slot(object)
    def __on_chat_select(self, cid: int) -> None: ...

    @Slot()
    def __on_chat_unselect(self) -> None: ...

    class StaminaPanel(QWidget):
        __bar: FruitFight2022GameInterface.StaminaHBar
        __label: QLabel
        __left: int
        __max: int

        def __init__(self, parent: QWidget) -> None: ...

        def __update_label(self) -> None: ...

        def set_left_max(self, left: int, mx: int) -> None: ...

        def set_left(self, left: int) -> None: ...

    class StaminaHBar(QWidget):
        __left: int
        __max: int

        def __init__(self, parent: QWidget) -> None: ...

        def paintEvent(self, event: QPaintEvent) -> None: ...

        @Slot(int, int)
        def set_left_max(self, left: int, mx: int) -> None: ...

        @Slot(int)
        def set_left(self, left: int) -> None: ...

    class GamePanel(QWidget):
        __stamina: FruitFight2022GameInterface.StaminaPanel
        __hands: 'FruitFight2022GameInterface.PlayersHands'

        def __init__(self, parent: QWidget) -> None: ...

        def set_data(self, data: GameState, max_stamina: int) -> None: ...

    class ChatItem:
        __cid: int
        __name: str
        __is_turn: bool
        __players_count: int

        __slots__ = ...

        def __init__(self, cid: int, name: str = "") -> None: ...

        @property
        def cid(self) -> int: ...

        @property
        def name(self) -> str: ...

        @name.setter
        def name(self, value: str) -> None: ...

        @property
        def is_turn(self) -> bool: ...

        @is_turn.setter
        def is_turn(self, value: bool) -> None: ...

        @property
        def players_count(self) -> int: ...

        @players_count.setter
        def players_count(self, value: int) -> None: ...

    class ChatsList(QWidget):
        __scrollbar: QScrollBar
        __canvas: 'FruitFight2022GameInterface.ChatsList.Canvas'

        selected = Signal(object)
        unselected = Signal()

        def __init__(self, parent) -> None: ...

        def move_cid_to_top(self, cid: int) -> None: ...

        def remove_cid(self, cid: int) -> None: ...

        def ensure_chat(self, chat: FruitFight2022GameInterface.ChatItem) -> None: ...

        @Slot(int, int, int)
        def __on_canvas_scroll(self, size: int, page: int, y: int) -> None: ...

        class Canvas(QWidget):
            __height: int
            __fheight: int
            __y: int
            __data: List[FruitFight2022GameInterface.ChatItem]
            __selected: Optional[int]
            __selected_signal: Signal
            __unselected_signal: Signal
            scrolled = Signal(int, int, int)

            @property
            def items_height(self) -> int: ...

            def __init__(self, parent, selected_signal: Signal, unselected_signal: Signal) -> None: ...

            def move_cid_to_top(self, cid: int) -> None: ...

            def paintEvent(self, event: QPaintEvent) -> None: ...

            def remove_cid(self, cid: int) -> None: ...

            def ensure_chat(self, chat: FruitFight2022GameInterface.ChatItem) -> None: ...

            def __draw_item(self, qp: QPainter, y: int, data: FruitFight2022GameInterface.ChatItem, is_selected: bool) -> None: ...

            def __calc_scroll(self) -> None: ...

            @Slot(int)
            def on_bar_scroll(self, y: int) -> None: ...

            def resizeEvent(self, event: QResizeEvent) -> None: ...

            def wheelEvent(self, event: QWheelEvent) -> None: ...

            def mousePressEvent(self, event: QMouseEvent) -> None: ...

    class BonesRow(QWidget):
        __data: Tuple[Bone, ...]

        def __init__(self, parent: QWidget): ...

        def resizeEvent(self, event: QResizeEvent) -> None: ...

        def __calc_size(self, height: int) -> None: ...

        @Slot(tuple)
        def set_data(self, data: Tuple[Bone, ...]) -> None: ...

        def paintEvent(self, event: QPaintEvent) -> None: ...

    class TurnPointer(QWidget):
        __is_on: bool

        def __init__(self, parent: QWidget) -> None: ...

        def heightForWidth(self, width: int) -> int: ...

        def set(self, value: bool) -> None: ...

        def paintEvent(self, event: QPaintEvent) -> None: ...

    class PlayersHands(QWidget):
        __layout: QGridLayout
        __pointers: List[FruitFight2022GameInterface.TurnPointer]
        __names: List[QLabel]
        __hands: List[FruitFight2022GameInterface.BonesRow]

        def set_row(self, index: int, turn: bool, name: str, hand: Tuple[Bone, ...]) -> None: ...

        def ensure_players_count(self, count: int) -> None: ...
