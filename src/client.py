import asyncio
import sys
import traceback

from PySide6.QtCore import QMutex, QObject, Signal, Slot
from telethon.sessions import MemorySession, SQLiteSession
from telethon import TelegramClient


class ClientWorker(QObject):
    def __init__(self):
        super().__init__()
        self.mutex = QMutex()
        self.aioloop = None
        self.telegram_client = None

    error_cc_happened = Signal(str)
    client_created = Signal()
    auth_complete = Signal()

    def __set_cc_error(self, message):
        self.error_cc_happened.emit(message)

    async def __create_client_async(self, api_id, api_hash, session):
        self.telegram_client = TelegramClient(
            session=session,
            api_id=api_id,
            api_hash=api_hash,
            loop=self.aioloop,
        )
        return await self.telegram_client.is_user_authorized()

    def __create_client(self, api_id, api_hash, session):
        if not self.mutex.tryLock(5):
            self.__set_cc_error("Failed to lock mutex")
            return
        try:
            if self.aioloop is None:
                self.aioloop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.aioloop)
            authorized = self.aioloop.run_until_complete(self.__create_client_async(api_id, api_hash, session))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.__set_cc_error(str(exc))
            return
        finally:
            self.mutex.unlock()
        if authorized:
            self.auth_complete.emit()
        else:
            self.client_created.emit()

    @Slot(str, str, str)
    def create_client_with_file(self, api_id, api_hash, path_to_auth_file):
        self.__create_client(api_id, api_hash, path_to_auth_file)

    @Slot(str, str)
    def create_client_in_memory(self, api_id, api_hash):
        self.__create_client(api_id, api_hash, MemorySession())

    error_aa_happened = Signal(str)
    requesting_code = Signal()

    def __set_aa_error(self, message):
        self.error_aa_happened.emit(message)

    @Slot(str)
    def send_phone(self, phone):
        try:
            self.aioloop.run_until_complete(self.telegram_client.send_code_request(phone))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.__set_aa_error(str(exc))
        else:
            self.requesting_code.emit()

    @Slot(str, str)
    def send_code_and_password(self, code, password):
        try:
            self.aioloop.run_until_complete(self.telegram_client.sign_in(code=code, password=password if password != "" else None))
        except Exception as exc:
            traceback.print_exception(exc, file=sys.stderr)
            self.__set_aa_error(str(exc))
        else:
            self.auth_complete.emit()
