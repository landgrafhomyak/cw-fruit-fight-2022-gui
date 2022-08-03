from asyncio import AbstractEventLoop
from typing import Optional, Union

from PySide2.QtCore import QMutex, QObject, QTimerEvent, Signal, Slot
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.tl.patched import Message
from telethon.tl.types.auth import SentCode

from game import ButtonWithBone, GameState, SkipTurnButton


class ClientWorker(QObject):
    mutex: QMutex
    telegram_client: Optional[TelegramClient]
    aioloop: Optional[AbstractEventLoop]

    def __init__(self) -> None: ...

    failed_creating_client = Signal(str)
    client_created = Signal()
    auth_completed = Signal()

    async def __create_client_async(self, api_id: str, api_hash: str, session: Union[str, MemorySession]) -> Optional[str]: ...

    def __create_client(self, api_id: str, api_hash: str, session: Union[str, MemorySession]) -> None: ...

    @Slot(str, str, str)
    def create_client_with_file(self, api_id: str, api_hash: str, path_to_auth_file: str) -> None: ...

    @Slot(str, str)
    def create_client_in_memory(self, api_id: str, api_hash: str) -> None: ...

    failed_sending_phone = Signal(str)
    requesting_code = Signal()
    failed_sending_code_and_password = Signal(str)

    @Slot(str)
    def send_phone(self, phone) -> None: ...

    async def __send_code_and_password_async(self, phone, code, password) -> str: ...

    @Slot(str, str, str)
    def send_code_and_password(self, phone, code, password) -> None: ...

    @Slot()
    def __start_receiving_updates(self) -> None: ...

    async def __get_and_process_updates(self) -> None: ...

    def timerEvent(self, event: QTimerEvent) -> None: ...

    chat_removing = Signal(object)
    sending_state = Signal(object, str, GameState)

    async def __message_handler(self, message: Message) -> None: ...

    async def __press_button(self, data: ButtonWithBone) -> None: ...

    @Slot(object)
    def press_button(self, data: Union[ButtonWithBone, SkipTurnButton]) -> None: ...
