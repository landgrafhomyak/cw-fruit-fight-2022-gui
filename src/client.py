import asyncio
import math
import sys
import time
import traceback

from PySide2.QtCore import QObject, Signal, Slot
from telethon.events import MessageEdited
from telethon.sessions import MemorySession
from telethon import TelegramClient

from game import GameState

_DELAY_S = 1


class ClientWorker(QObject):
    def __init__(self):
        super().__init__()
        # self.mutex = QMutex()
        self.aioloop = None
        self.telegram_client = None
        self.auth_completed.connect(self.__start_receiving_updates)

    failed_creating_client = Signal(str)
    client_created = Signal()
    auth_completed = Signal(str)

    async def __create_client_async(self, api_id, api_hash, session):
        self.telegram_client = TelegramClient(
            session=session,
            api_id=api_id,
            api_hash=api_hash,
            loop=self.aioloop,
            receive_updates=False
        )
        await self.telegram_client.connect()
        if not await self.telegram_client.is_user_authorized():
            return None

        self.telegram_client.on(MessageEdited(from_users=5265011919))(self.__message_handler)

        user = await self.telegram_client.get_me()
        return user.first_name if user.first_name is not None else "" + " " + user.last_name if user.last_name is not None else ""

    def __create_client(self, api_id, api_hash, session):
        # if not self.mutex.tryLock(5):
        #     self.__set_cc_error("Failed to lock mutex")
        #     return
        try:
            if self.aioloop is None:
                self.aioloop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.aioloop)
            full_name = self.aioloop.run_until_complete(self.__create_client_async(api_id, api_hash, session))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.failed_creating_client.emit(str(exc))
            return
        # finally:
        #     self.mutex.unlock()

        if full_name is not None:
            self.auth_completed.emit(full_name)
        else:
            self.client_created.emit()

    @Slot(str, str, str)
    def create_client_with_file(self, api_id, api_hash, path_to_auth_file):
        self.__create_client(api_id, api_hash, path_to_auth_file)

    @Slot(str, str)
    def create_client_in_memory(self, api_id, api_hash):
        self.__create_client(api_id, api_hash, MemorySession())

    failed_sending_phone = Signal(str)
    requesting_code = Signal()
    failed_sending_code_and_password = Signal(str)

    @Slot(str)
    def send_phone(self, phone):
        try:
            self.aioloop.run_until_complete(self.telegram_client.send_code_request(phone))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.failed_sending_phone.emit(str(exc))
            return
        else:
            self.requesting_code.emit()

    async def __send_code_and_password_async(self, phone, code, password):
        await self.telegram_client.sign_in(phone=phone, code=code, password=password if password != "" else None)
        user = await self.telegram_client.get_me()
        return user.first_name if user.first_name is not None else "" + " " + user.last_name if user.last_name is not None else ""

    @Slot(str, str, str)
    def send_code_and_password(self, phone, code, password):
        try:
            full_name = self.aioloop.run_until_complete(self.__send_code_and_password_async(phone, code, password))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.failed_sending_code_and_password.emit(str(exc))
        else:
            self.auth_completed.emit(full_name)

    @Slot()
    def __start_receiving_updates(self):
        self.startTimer(math.ceil(_DELAY_S * 1000))

    @staticmethod
    async def __get_and_process_updates():
        end_time = time.time() + _DELAY_S - 0.1
        while time.time() < end_time:
            await asyncio.sleep(0)

    def timerEvent(self, event):
        try:
            self.aioloop.run_until_complete(self.__get_and_process_updates())
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)

    chat_removing = Signal(object)
    sending_state = Signal(object, str, GameState)

    async def __message_handler(self, message):
        state = GameState(message.raw_text)
        if state is None:
            return

        if state.is_ended:
            self.chat_removing.emit(message.chat_id)
            return
        else:
            self.sending_state.emit(message.chat_id, message.chat.title, state)
