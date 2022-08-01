import asyncio
import sys
import traceback

from PySide6.QtCore import QMutex, QObject, Signal, Slot
from telethon.sessions import MemorySession, SQLiteSession
from telethon import TelegramClient


class ClientWorker(QObject):
    def __init__(self):
        super().__init__()
        # self.mutex = QMutex()
        self.aioloop = None
        self.telegram_client = None

    failed_creating_client = Signal(str)
    client_created = Signal()
    auth_completed = Signal()

    async def __create_client_async(self, api_id, api_hash, session):
        self.telegram_client = TelegramClient(
            session=session,
            api_id=api_id,
            api_hash=api_hash,
            loop=self.aioloop,
        )
        await self.telegram_client.connect()
        return await self.telegram_client.is_user_authorized()

    def __create_client(self, api_id, api_hash, session):
        # if not self.mutex.tryLock(5):
        #     self.__set_cc_error("Failed to lock mutex")
        #     return
        try:
            if self.aioloop is None:
                self.aioloop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.aioloop)
            authorized = self.aioloop.run_until_complete(self.__create_client_async(api_id, api_hash, session))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.failed_creating_client.emit(str(exc))
            return
        # finally:
        #     self.mutex.unlock()

        if authorized:
            self.auth_completed.emit()
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

    @Slot(str, str, str)
    def send_code_and_password(self, phone, code, password):
        try:
            self.aioloop.run_until_complete(self.telegram_client.sign_in(phone=phone, code=code, password=password if password != "" else None))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.failed_sending_code_and_password.emit(str(exc))
        else:
            self.auth_completed.emit()
