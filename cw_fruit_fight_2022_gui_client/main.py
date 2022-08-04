from PySide2.QtWidgets import QApplication

from .gui import Cwff2022gcMainWindow
from .client import Cwff2022gcClientThread, Cwff2022gcClientWorker


def main(args) -> int:
    qapp = QApplication([])
    client = Cwff2022gcClientWorker(None)
    thread = Cwff2022gcClientThread(client)
    client.moveToThread(thread)
    thread.start()
    window = Cwff2022gcMainWindow(client)
    window.show()

    return qapp.exec_()


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
