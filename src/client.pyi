from typing import NoReturn, Optional

from PySide6.QtCore import QMutex, QObject, QThread, Signal, Slot
from telethon.sync import TelegramClient

from src.gui import FruitFight2022AuthDialog


class ClientThreadBase(QThread):
    mutex: QMutex
    telegram_client: Optional[TelegramClient]

    def __init__(self) -> None: ...


class ClientAuthAndCreate(ClientThreadBase):
    error_happened = Signal(str)

    @property
    def client_config_window(self) -> NoReturn: ...

    @client_config_window.setter
    def client_config_window(self, value: FruitFight2022AuthDialog.ClientConfiguration) -> None: ...

    def __init__(self) -> None: ...

    def __set_error(self, message) -> None: ...

    @Slot(str, str, str)
    def create_client_with_file(self, api_id: str, api_hash: str, path_to_auth_file: str) -> None: ...

    @Slot(str, str)
    def create_client_in_memory(self, api_id: str, api_hash: str) -> None: ...


class ClientThread(ClientAuthAndCreate, ClientThreadBase):
    pass
