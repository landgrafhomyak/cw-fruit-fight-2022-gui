from PySide6.QtWidgets import QApplication, QMainWindow

from gui import FruitFight2022MainWindow
from src.client import ClientThread


def main(args) -> int:
    qapp = QApplication([])
    thread = ClientThread()

    window = FruitFight2022MainWindow(thread)
    window.show()
    return qapp.exec()

if __name__ == "__main__":
    import sys

    exit(main(sys.argv))
