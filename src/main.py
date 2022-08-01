from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication

from gui import FruitFight2022MainWindow
from src.client import ClientWorker


def main(args) -> int:
    qapp = QApplication([])
    client = ClientWorker()
    thread = QThread()
    window = FruitFight2022MainWindow(client)
    client.moveToThread(thread)
    thread.start(QThread.IdlePriority)
    window.show()

    return qapp.exec()


if __name__ == "__main__":
    import sys

    exit(main(sys.argv))
