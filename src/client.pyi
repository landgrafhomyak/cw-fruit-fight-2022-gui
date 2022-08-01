from typing import  Optional

from PySide6.QtCore import QMutex, QObject, Signal, Slot
from telethon.sync import TelegramClient


class ClientWorker(QObject):
    mutex: QMutex
    telegram_client: Optional[TelegramClient]

    def __init__(self) -> None: ...

    error_happened = Signal(str)
    client_created = Signal()

    def __set_error(self, message) -> None: ...

    @Slot(str, str, str)
    def create_client_with_file(self, api_id: str, api_hash: str, path_to_auth_file: str) -> None: ...

    @Slot(str, str)
    def create_client_in_memory(self, api_id: str, api_hash: str) -> None: ...
