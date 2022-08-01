from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QButtonGroup, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget

from src.client import ClientWorker


class FruitFight2022MainWindow(QMainWindow):
    __client_config_tab: FruitFight2022ClientConfiguration
    __account_auth_tab: FruitFight2022AccountAuth

    def __init__(self, client_worker: ClientWorker) -> None: ...

    @Slot
    def __on_client_created(self) -> None: ...


class FruitFight2022ClientConfiguration(QWidget):
    __api_id_input: QLineEdit
    __api_hash_input: QLineEdit
    __rb_group: QButtonGroup
    __file_input: QLineEdit
    __file_input_button: QPushButton
    __message_label: QLabel

    in_memory_client_creating = Signal(str, str)
    file_client_creating = Signal(str, str, str)

    def __init__(self, parent: FruitFight2022MainWindow, client_worker: ClientWorker) -> None: ...

    @Slot()
    def __create_client(self): ...

    @Slot(str)
    def __set_error_message(self, text) -> None: ...


class FruitFight2022AccountAuth(QWidget):
    def __init__(self, parent: FruitFight2022MainWindow, client_worker: ClientWorker) -> None: ...
