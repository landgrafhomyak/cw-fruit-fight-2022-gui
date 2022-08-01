from PySide6.QtCore import QMutex, QThread, Signal, Slot
from telethon.sessions import MemorySession
from telethon.sync import TelegramClient


class ClientThreadBase(QThread):
    def __init__(self):
        super().__init__()
        self.mutex = QMutex()
        self.telegram_client = None


class ClientAuthAndCreate(ClientThreadBase):
    error_happened = Signal(str)

    def __set_error(self, message):
        self.error_happened.emit(message)

    @Slot(str, str, str)
    def create_client_with_file(self, api_id, api_hash, path_to_auth_file):
        if not self.mutex.tryLock(5):
            self.__set_error("Failed to lock mutex")
            return
        try:
            self.telegram_client = TelegramClient(
                session=path_to_auth_file,
                api_id=api_id,
                api_hash=api_hash
            )
        except Exception as exc:
            self.__set_error(str(exc))

        finally:
            self.mutex.unlock()

    @Slot(str, str)
    def create_client_in_memory(self, api_id, api_hash):
        if not self.mutex.tryLock(5):
            self.__set_error("Failed to lock mutex")
            return
        try:
            self.telegram_client = TelegramClient(
                session=MemorySession(),
                api_id=api_id,
                api_hash=api_hash
            )
        except Exception as exc:
            self.__set_error(str(exc))

        finally:
            self.mutex.unlock()


class ClientThread(ClientAuthAndCreate, ClientThreadBase):
    pass
