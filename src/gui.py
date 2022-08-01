from PySide6.QtCore import Qt
from PySide6.QtWidgets import QButtonGroup, QCheckBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QRadioButton, QSizePolicy, QStackedLayout, QVBoxLayout, QWidget


class FruitFight2022MainWindow(QMainWindow):
    # __slots__ = ("client_config_tab",)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatWars Fruit fight 2022 GUI Client")
        self.client_config_tab = FruitFight2022AuthDialog()
        self.setCentralWidget(self.client_config_tab)


class FruitFight2022AuthDialog(QWidget):
    class ClientConfiguration(QWidget):
        def __init__(self):
            super().__init__()
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            layout = QGridLayout(self)
            self.setLayout(layout)
            layout.setColumnStretch(0, 0)
            layout.setColumnStretch(1, 1)
            layout.setColumnStretch(2, 0)

            layout.addWidget(QLabel("Client configuration (<a href=\"https://my.telegram.org/apps\">https://my.telegram.org/apps</a>)", self), 0, 0, 1, 3, Qt.AlignLeft)

            layout.addWidget(QLabel("API ID:", self), 1, 0, Qt.AlignRight)
            self.api_id_input = QLineEdit()
            self.api_id_input.setEchoMode(QLineEdit.Password)
            self.api_id_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout.addWidget(self.api_id_input, 1, 1, 1, 2)

            layout.addWidget(QLabel("API Hash:", self), 2, 0, Qt.AlignRight)
            self.api_hash_input = QLineEdit()
            self.api_hash_input.setEchoMode(QLineEdit.Password)
            self.api_hash_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout.addWidget(self.api_hash_input, 2, 1, 1, 2)

            rb1 = QRadioButton("In-memory auth file (requires re-auth on each app launch)", self)
            rb1.setChecked(True)
            rb2 = QRadioButton("Auth file on disk (will be created if not exists)", self)
            group = QButtonGroup()
            group.addButton(rb1)
            group.addButton(rb2)
            rb_layout = QHBoxLayout()
            layout.addLayout(rb_layout, 3, 0, 1, 3, Qt.AlignHCenter)
            rb_layout.addWidget(rb1, alignment=Qt.AlignRight)
            rb_layout.addWidget(rb2, alignment=Qt.AlignLeft)

            layout.addWidget(QLabel("Path to auth file:", self), 4, 0, Qt.AlignRight)
            self.file_input = QLineEdit(self)
            self.file_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.file_input.setDisabled(True)
            layout.addWidget(self.file_input, 4, 1)
            self.file_input_button = QPushButton("...", self)
            self.file_input_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            self.file_input_button.setDisabled(True)
            layout.addWidget(self.file_input_button, 4, 2)

            self.message_label = QLabel(self)
            self.message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            layout.addWidget(self.message_label, 5, 0, 1, 3)

            exit_button = QPushButton("Exit", self)
            create_button = QPushButton("Create client", self)
            buttons_layout = QHBoxLayout(self)
            buttons_layout.addWidget(exit_button, 0, Qt.AlignLeft)
            buttons_layout.addStretch(1)
            buttons_layout.addWidget(create_button, 0, Qt.AlignRight)
            layout.addLayout(buttons_layout, 6, 0, 1, 3)

            # layout.addWidget(check_box)

    # __slots__ = ("client_config",)

    def __init__(self):
        super().__init__()

        self.client_config = FruitFight2022AuthDialog.ClientConfiguration()

        layout = QVBoxLayout(self)
        layout.addWidget(self.client_config)
        self.setLayout(layout)
