from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QCloseEvent, QColor, QPalette
from PySide6.QtWidgets import QApplication, QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QRadioButton, QSizePolicy, QWidget


class FruitFight2022MainWindow(QMainWindow):
    closed = Signal()

    def __init__(self, client_worker):
        super().__init__()
        self.__client_worker = client_worker
        self.setWindowTitle("ChatWars Fruit fight 2022 GUI Client")
        self.__client_config_tab = FruitFight2022ClientConfiguration(self, client_worker)
        self.__account_auth_tab = FruitFight2022AccountAuth(self, client_worker)
        # self.setCentralWidget(self.__client_config_tab)
        self.setCentralWidget(self.__account_auth_tab)
        client_worker.client_created.connect(self.__on_client_created)

    @Slot()
    def __on_client_created(self):
        self.setCentralWidget(self.__account_auth_tab)

    def closeEvent(self, event=None):
        QApplication.exit(0)


class FruitFight2022ClientConfiguration(QWidget):
    in_memory_client_creating = Signal(str, str)
    file_client_creating = Signal(str, str, str)

    def __init__(self, parent, client_worker):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QGridLayout(self)
        self.setLayout(layout)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 0)

        layout.addWidget(QLabel("Client configuration (<a href=\"https://my.telegram.org/apps\">https://my.telegram.org/apps</a>)", self), 0, 0, 1, 3, Qt.AlignLeft)

        layout.addWidget(QLabel("API ID:", self), 1, 0, Qt.AlignRight)
        self.__api_id_input = QLineEdit()
        self.__api_id_input.setEchoMode(QLineEdit.Password)
        self.__api_id_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__api_id_input, 1, 1, 1, 2)

        layout.addWidget(QLabel("API Hash:", self), 2, 0, Qt.AlignRight)
        self.__api_hash_input = QLineEdit()
        self.__api_hash_input.setEchoMode(QLineEdit.Password)
        self.__api_hash_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__api_hash_input, 2, 1, 1, 2)

        rb1 = QRadioButton("In-memory auth file (requires re-auth on each app launch)", self)
        rb1.setChecked(True)
        rb2 = QRadioButton("Auth file on disk (will be created if not exists)", self)
        self.__rb_group = QButtonGroup()
        self.__rb_group.addButton(rb1, 0)
        self.__rb_group.addButton(rb2, 1)
        rb_layout = QHBoxLayout()
        layout.addLayout(rb_layout, 3, 0, 1, 3, Qt.AlignHCenter)
        rb_layout.addWidget(rb1, alignment=Qt.AlignRight)
        rb_layout.addWidget(rb2, alignment=Qt.AlignLeft)

        self.__file_label = QLabel("Path to auth file:", self)
        self.__file_label.setEnabled(False)
        layout.addWidget(self.__file_label, 4, 0, Qt.AlignRight)
        self.__file_input = QLineEdit(self)
        self.__file_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__file_input.setEnabled(False)
        layout.addWidget(self.__file_input, 4, 1)
        self.__file_button = QPushButton("...", self)
        self.__file_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.__file_button.setEnabled(False)
        layout.addWidget(self.__file_button, 4, 2)

        self.__message_label = QLabel(self)
        _palette = QPalette()
        _palette.setColor(QPalette.WindowText, QColor("red"))
        self.__message_label.setPalette(_palette)
        self.__message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__message_label, 5, 0, 1, 3)

        exit_button = QPushButton("Exit", self)
        create_button = QPushButton("Create client", self)
        buttons_layout = QHBoxLayout(self)
        buttons_layout.addWidget(exit_button, 0, Qt.AlignLeft)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(create_button, 0, Qt.AlignRight)
        layout.addLayout(buttons_layout, 6, 0, 1, 3)

        exit_button.clicked.connect(parent.close)
        create_button.clicked.connect(self.__create_client)
        client_worker.error_happened.connect(self.__set_error_message)
        self.in_memory_client_creating.connect(client_worker.create_client_in_memory)
        self.file_client_creating.connect(client_worker.create_client_with_file)

    @Slot()
    def __create_client(self):
        button = self.__rb_group.checkedId()
        self.__message_label.setText("")
        if button == 0:
            self.in_memory_client_creating.emit(
                self.__api_id_input.text(),
                self.__api_hash_input.text()
            )
        elif button == 1:
            self.file_client_creating.emit(
                self.__api_id_input.text(),
                self.__api_hash_input.text(),
                self.__file_input.text(),
            )
        else:
            self.__set_error_message("Client storage not selected (2 radio buttons)")

    @Slot(str)
    def __set_error_message(self, text):
        self.__message_label.setText(text)


class FruitFight2022AccountAuth(QWidget):
    def __init__(self, parent, client_worker):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QGridLayout(self)
        self.setLayout(layout)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 0)

        self.__phone_label = QLabel("Phone:", self)
        layout.addWidget(self.__phone_label, 0, 0, Qt.AlignRight)
        self.__phone_input = QLineEdit(self)
        self.__phone_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__phone_input, 0, 1)
        self.__phone_button = QPushButton("Send code", self)
        self.__phone_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__phone_button, 0, 2)

        self.__code_label = QLabel("Code:", self)
        self.__code_label.setEnabled(False)
        layout.addWidget(self.__code_label, 1, 0, Qt.AlignRight)
        self.__code_input = QLineEdit(self)
        self.__code_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__code_input.setEchoMode(QLineEdit.Password)
        self.__code_input.setEnabled(False)
        layout.addWidget(self.__code_input, 1, 1)
        self.__code_button = QPushButton("Check code", self)
        self.__code_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__code_button.setEnabled(False)
        layout.addWidget(self.__code_button, 1, 2)

        self.__password_label = QLabel("Password:", self)
        self.__password_label.setEnabled(False)
        layout.addWidget(self.__password_label, 2, 0, Qt.AlignRight)
        self.__password_input = QLineEdit(self)
        self.__password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__password_input.setEchoMode(QLineEdit.Password)
        self.__password_input.setEnabled(False)
        layout.addWidget(self.__password_input, 2, 1)
        self.__password_button = QPushButton("Enter password", self)
        self.__password_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__password_button.setEnabled(False)
        layout.addWidget(self.__password_button, 2, 2)

        self.__message_label = QLabel(self)
        _palette = QPalette()
        _palette.setColor(QPalette.WindowText, QColor("red"))
        self.__message_label.setPalette(_palette)
        self.__message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__message_label, 3, 0, 1, 3)

        prev_button = QPushButton("Back", self)
        self.__reenter_phone_button = QPushButton("Change phone", self)
        self.__reenter_phone_button.setEnabled(False)
        buttons_layout = QHBoxLayout(self)
        buttons_layout.addWidget(prev_button, 0, Qt.AlignLeft)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.__reenter_phone_button, 0, Qt.AlignHCenter)
        buttons_layout.addStretch(2)
        layout.addLayout(buttons_layout, 4, 0, 1, 3)
