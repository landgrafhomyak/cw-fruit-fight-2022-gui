import asyncio

from PySide6.QtCore import QMutex, QObject, QThread, Signal, Slot
from telethon.sessions import MemorySession
from telethon import TelegramClient


class ClientWorker(QObject):
    error_happened = Signal(str)
    client_created = Signal()

    def __init__(self):
        super().__init__()
        self.mutex = QMutex()
        self.aioloop = None
        self.telegram_client = None

    def __set_error(self, message):
        self.error_happened.emit(message)

    async def __create_client_async(self, api_id, api_hash, session):
        self.telegram_client = TelegramClient(
            session=session,
            api_id=api_id,
            api_hash=api_hash,
            loop=self.aioloop
        )

    def __create_client(self, api_id, api_hash, session):
        if not self.mutex.tryLock(5):
            self.__set_error("Failed to lock mutex")
            return
        try:
            if self.aioloop is None:
                self.aioloop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.aioloop)
            self.aioloop.run_until_complete(self.__create_client_async(api_id, api_hash, session))
        except Exception as exc:
            self.__set_error(str(exc))
        finally:
            self.mutex.unlock()
        self.client_created.emit()

    @Slot(str, str, str)
    def create_client_with_file(self, api_id, api_hash, path_to_auth_file):
        self.__create_client(api_id, api_hash, path_to_auth_file)

    @Slot(str, str)
    def create_client_in_memory(self, api_id, api_hash):
        self.__create_client(api_id, api_hash, MemorySession())
