from asyncio import AbstractEventLoop
from typing import Optional, Union

from PySide6.QtCore import QMutex, QObject, Signal, Slot
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.tl.types.auth import SentCode


class ClientWorker(QObject):
    mutex: QMutex
    telegram_client: Optional[TelegramClient]
    aioloop: Optional[AbstractEventLoop]

    def __init__(self) -> None: ...

    error_cc_happened = Signal(str)
    client_created = Signal()
    auth_complete = Signal()

    def __set_cc_error(self, message) -> None: ...

    async def __create_client_async(self, api_id: str, api_hash: str, session: Union[str, MemorySession]) -> None: ...

    def __create_client(self, api_id: str, api_hash: str, session: Union[str, MemorySession]) -> None: ...

    @Slot(str, str, str)
    def create_client_with_file(self, api_id: str, api_hash: str, path_to_auth_file: str) -> None: ...

    @Slot(str, str)
    def create_client_in_memory(self, api_id: str, api_hash: str) -> None: ...

    error_aa_happened = Signal(str)
    requesting_code = Signal()

    def __set_aa_error(self, message) -> None: ...

    @Slot(str)
    def send_phone(self, phone) -> None: ...

    @Slot(str, str)
    def send_code_and_password(self, code, password) -> None: ...
