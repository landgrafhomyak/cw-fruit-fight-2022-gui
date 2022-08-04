from typing import Optional

from cw_fruit_fight_2022_gui_client import Cwff2022gcGameState
from PySide2.QtCore import QObject, QThread, Signal
from qasync import asyncSlot as AsyncSlot


class Cwff2022gcClientThread(QThread):
    def __init__(self, parent: Optional[QObject] = None) -> None: ...

    def run(self) -> None: ...


class Cwff2022gcClientWorker(QObject):
    def __init__(self, parent: Optional[QObject] = None) -> None: ...

    client_created_need_auth = Signal()
    client_created_auth_complete = Signal(str)
    client_creation_error = Signal(str)

    @AsyncSlot(str, str)
    async def create_client_in_memory(self, api_id: str, api_hash: str) -> None: ...

    @AsyncSlot(str, str, str)
    async def create_client_with_file(self, api_id: str, api_hash: str, file_path: str) -> None: ...

    phone_sent = Signal()
    signed_in = Signal(str)
    sending_phone_error = Signal(str)
    signing_in_error = Signal(str)

    @AsyncSlot(str)
    async def send_phone(self, phone: str) -> None: ...

    @AsyncSlot(str, str, str)
    async def send_code_and_password(self, phone: str, code: str, password: str) -> None: ...

    chat_removed = Signal(object)
    chat_updated = Signal(object, str, Cwff2022gcGameState)

    @AsyncSlot(object)
    async def press_button(self, data) -> None: ...
