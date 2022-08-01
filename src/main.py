from PySide6.QtWidgets import QApplication, QMainWindow

from gui import FruitFight2022MainWindow


def main(args) -> int:
    qapp = QApplication([])
    window = FruitFight2022MainWindow()
    window.show()
    return qapp.exec()

if __name__ == "__main__":
    import sys

    exit(main(sys.argv))
