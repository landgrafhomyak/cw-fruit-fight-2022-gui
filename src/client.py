from PySide6.QtCore import QThread, Slot


class ClientThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)

    @Slot(int, str)
    def create_client(self):
        pass