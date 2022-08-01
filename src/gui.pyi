from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QButtonGroup, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget

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
    __api_id_input: QLineEdit
    __api_hash_input: QLineEdit
    __rb_group: QButtonGroup
    __file_label: QLabel
    __file_input: QLineEdit
    __file_button: QPushButton
    __message_label: QLabel

    in_memory_client_creating = Signal(str, str)
    file_client_creating = Signal(str, str, str)

    def __init__(self, parent: FruitFight2022MainWindow, client_worker: ClientWorker) -> None: ...

    @Slot()
    def __create_client(self): ...

    @Slot(str)
    def __set_error_message(self, text) -> None: ...


class FruitFight2022AccountAuth(QWidget):
    __phone_label: QLabel
    __phone_input: QLineEdit
    __phone_button: QPushButton
    __code_label: QLabel
    __code_input: QLineEdit
    __change_phone: QPushButton
    __password_label: QLabel
    __password_input: QLineEdit
    __auth: QPushButton
    __message_label: QLabel

    sending_phone = Signal(str)
    sending_code_and_password = Signal(str, str)

    def __init__(self, parent: FruitFight2022MainWindow, client_worker: ClientWorker) -> None: ...

    @Slot(str)
    def __set_error_message(self, message: str) -> None: ...

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
    pass
