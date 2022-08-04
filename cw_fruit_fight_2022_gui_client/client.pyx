import asyncio
import sys
import traceback

from cw_fruit_fight_2022_gui_client.game import Cwff2022gcGameState
from PySide2.QtCore import QObject, QThread, Signal
from qasync import asyncSlot as AsyncSlot, QEventLoop
from telethon import TelegramClient
from telethon.events import MessageEdited
from telethon.sessions import MemorySession


class Cwff2022gcClientThread(QThread):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__aioloop = None

    def run(self):
        self.__aioloop = QEventLoop(self)
        asyncio.set_event_loop(self.__aioloop)
        self.__aioloop.run_forever()


class Cwff2022gcClientWorker(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__client = None

    client_created_need_auth = Signal()
    client_created_auth_complete = Signal(str)
    client_creation_error = Signal(str)

    async def __create_client(self, api_id, api_hash, session):
        if self.__client is not None:
            raise RuntimeError("Telegram client already exists")
        try:
            self.__client = TelegramClient(
                api_id=api_id,
                api_hash=api_hash,
                session=session
            )
            self.__client.on(MessageEdited(from_users=5265011919))(self.__message_handler)

            await self.__client.connect()
            if not await self.__client.is_user_authorized():
                self.client_created_need_auth.emit()
                return None

            user = await self.__client.get_me()
            self.client_created_auth_complete.emit((user.first_name or "") + " " + (user.last_name or ""))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.client_creation_error.emit(str(exc))

    @AsyncSlot(str, str)
    async def create_client_in_memory(self, api_id, api_hash):
        await self.__create_client(api_id, api_hash, MemorySession())

    @AsyncSlot(str, str, str)
    async def create_client_with_file(self, api_id, api_hash, file_path):
        await self.__create_client(api_id, api_hash, file_path)

    phone_sent = Signal()
    signed_in = Signal(str)
    sending_phone_error = Signal(str)
    signing_in_error = Signal(str)

    @AsyncSlot(str)
    async def send_phone(self, phone: str):
        try:
            await self.__client.send_code_request(phone)
            self.phone_sent.emit()
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.sending_phone_error.emit(str(exc))

    @AsyncSlot(str, str, str)
    async def send_code_and_password(self, phone: str, code: str, password: str):
        try:
            await self.__client.sign_in(
                phone=phone,
                code=code,
                password=password or None
            )
            user = await self.__client.get_me()
            self.signed_in.emit((user.first_name or "") + " " + (user.last_name or ""))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.signing_in_error.emit(str(exc))

    chat_removed = Signal(object)
    chat_updated = Signal(object, str, Cwff2022gcGameState)

    async def __message_handler(self, message):
        try:
            state = Cwff2022gcGameState(message.raw_text, message.buttons)
            if state is None:
                return

            if state.is_ended:
                self.chat_updated.emit(message.chat_id, message.chat.title, state)
                self.chat_removed.emit(message.chat_id)
                return
            else:
                self.chat_updated.emit(message.chat_id, message.chat.title, state)
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)

    @AsyncSlot(object)
    async def press_button(self, data):
        try:
            await data.button.click()
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
