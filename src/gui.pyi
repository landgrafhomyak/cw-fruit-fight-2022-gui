from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QButtonGroup, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget

from src.client import ClientThread, ClientAuthAndCreate


class FruitFight2022MainWindow(QMainWindow):
    client_config_tab: FruitFight2022AuthDialog

    def __init__(self, client_thread: ClientThread) -> None: ...


class FruitFight2022AuthDialog(QWidget):
    client_config: 'FruitFight2022AuthDialog.ClientConfiguration'

    def __init__(self, client_thread: ClientThread) -> None: ...

    class ClientConfiguration(QWidget):
        __api_id_input: QLineEdit
        __api_hash_input: QLineEdit
        __rb_group: QButtonGroup
        __file_input: QLineEdit
        __file_input_button: QPushButton
        __message_label: QLabel
        __client_thread: ClientAuthAndCreate

        in_memory_client_creating = Signal(str, str)
        file_client_creating = Signal(str, str, str)

        def __init__(self, client_thread: ClientAuthAndCreate) -> None: ...

        @Slot()
        def __create_client(self): ...

        @Slot(str)
        def __set_error_message(self, text) -> None: ...
