from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QCloseEvent, QColor, QPalette
from PySide6.QtWidgets import QApplication, QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QRadioButton, QSizePolicy, QToolButton, QWidget


class FruitFight2022MainWindow(QMainWindow):
    closed = Signal()

    def __init__(self, client_worker):
        super().__init__()
        self.__client_worker = client_worker
        self.setWindowTitle("ChatWars Fruit fight 2022 GUI Client")
        self.__client_config_tab = FruitFight2022ClientConfiguration(self, client_worker)
        self.__account_auth_tab = FruitFight2022AccountAuth(self, client_worker)
        self.__game_interface_tab = FruitFight2022GameInterface(self)
        self.setCentralWidget(self.__client_config_tab)
        client_worker.client_created.connect(self.__on_client_created)
        client_worker.auth_completed.connect(self.__on_auth_completed)

    @Slot()
    def __on_client_created(self):
        self.setCentralWidget(self.__account_auth_tab)

    @Slot()
    def re_create_client(self):
        self.setCentralWidget(self.__client_config_tab)

    def closeEvent(self, event=None):
        QApplication.exit(0)

    @Slot()
    def __on_auth_completed(self):
        self.setCentralWidget(self.__game_interface_tab)


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

        self.__api_id_label = QLabel("API ID:", self)
        layout.addWidget(self.__api_id_label, 1, 0, Qt.AlignRight)
        self.__api_id_input = QLineEdit()
        self.__api_id_input.setEchoMode(QLineEdit.Password)
        self.__api_id_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__api_id_input, 1, 1, 1, 2)

        self.__api_hash_label = QLabel("API Hash:", self)
        layout.addWidget(self.__api_hash_label, 2, 0, Qt.AlignRight)
        self.__api_hash_input = QLineEdit()
        self.__api_hash_input.setEchoMode(QLineEdit.Password)
        self.__api_hash_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__api_hash_input, 2, 1, 1, 2)

        self.__rb_inmemory = QRadioButton("In-memory auth file (requires re-auth on each app launch)", self)
        self.__rb_inmemory.setChecked(True)
        self.__rb_file = QRadioButton("Auth file on disk (will be created if not exists)", self)
        self.__rb_group = QButtonGroup()
        self.__rb_group.addButton(self.__rb_inmemory, 0)
        self.__rb_group.addButton(self.__rb_file, 1)
        rb_layout = QHBoxLayout()
        layout.addLayout(rb_layout, 3, 0, 1, 3, Qt.AlignHCenter)
        rb_layout.addWidget(self.__rb_inmemory, alignment=Qt.AlignRight)
        rb_layout.addWidget(self.__rb_file, alignment=Qt.AlignLeft)

        self.__file_label = QLabel("Path to auth file:", self)
        self.__file_label.setEnabled(False)
        layout.addWidget(self.__file_label, 4, 0, Qt.AlignRight)
        self.__file_input = QLineEdit(self)
        self.__file_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__file_input.setEnabled(False)
        layout.addWidget(self.__file_input, 4, 1)
        self.__file_button = QToolButton(self)
        self.__file_button.setText("...")
        self.__file_button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.__file_button.setEnabled(False)
        layout.addWidget(self.__file_button, 4, 2)

        self.__message_label = QLabel(self)
        _palette = QPalette()
        _palette.setColor(QPalette.WindowText, QColor("red"))
        self.__message_label.setPalette(_palette)
        self.__message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__message_label, 5, 0, 1, 3)

        exit_button = QPushButton("Exit", self)
        self.__create_client_button = QPushButton("Create client", self)
        buttons_layout = QHBoxLayout(self)
        buttons_layout.addWidget(exit_button, 0, Qt.AlignLeft)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.__create_client_button, 0, Qt.AlignRight)
        layout.addLayout(buttons_layout, 6, 0, 1, 3)

        exit_button.clicked.connect(parent.close)
        self.__create_client_button.clicked.connect(self.__create_client)
        client_worker.failed_creating_client.connect(self.__on_client_creation_fail)
        self.in_memory_client_creating.connect(client_worker.create_client_in_memory)
        self.file_client_creating.connect(client_worker.create_client_with_file)
        self.__rb_inmemory.clicked.connect(self.__inmemory_variant)
        self.__rb_file.clicked.connect(self.__file_variant)

    @Slot()
    def __create_client(self):
        self.__api_id_label.setEnabled(False)
        self.__api_id_input.setEnabled(False)
        self.__api_hash_label.setEnabled(False)
        self.__api_hash_input.setEnabled(False)
        self.__rb_inmemory.setEnabled(False)
        self.__rb_file.setEnabled(False)
        self.__file_label.setEnabled(False)
        self.__file_input.setEnabled(False)
        self.__file_button.setEnabled(False)
        self.__create_client_button.setEnabled(False)
        self.__message_label.setText("")
        button = self.__rb_group.checkedId()
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
            self.__on_client_creation_fail("Client storage not selected (2 radio buttons)")

    @Slot(str)
    def __on_client_creation_fail(self, text):
        self.__message_label.setText(text)
        self.__api_id_label.setEnabled(True)
        self.__api_id_input.setEnabled(True)
        self.__api_hash_label.setEnabled(True)
        self.__api_hash_input.setEnabled(True)
        self.__rb_inmemory.setEnabled(True)
        self.__rb_file.setEnabled(True)
        if self.__rb_group.checkedId() == 1:
            self.__file_label.setEnabled(True)
            self.__file_input.setEnabled(True)
            self.__file_button.setEnabled(True)
        self.__create_client_button.setEnabled(True)

    @Slot()
    def __inmemory_variant(self):
        self.__file_label.setEnabled(False)
        self.__file_input.setEnabled(False)
        self.__file_button.setEnabled(False)

    @Slot()
    def __file_variant(self):
        self.__file_label.setEnabled(True)
        self.__file_input.setEnabled(True)
        self.__file_button.setEnabled(True)


class FruitFight2022AccountAuth(QWidget):
    sending_phone = Signal(str)
    sending_code_and_password = Signal(str, str, str)

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
        self.__change_phone_button = QPushButton("Change phone", self)
        self.__change_phone_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__change_phone_button.setEnabled(False)
        layout.addWidget(self.__change_phone_button, 1, 2)

        self.__password_label = QLabel("Password:", self)
        self.__password_label.setEnabled(False)
        layout.addWidget(self.__password_label, 2, 0, Qt.AlignRight)
        self.__password_input = QLineEdit(self)
        self.__password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__password_input.setEchoMode(QLineEdit.Password)
        self.__password_input.setEnabled(False)
        layout.addWidget(self.__password_input, 2, 1)
        self.__auth = QPushButton("Auth", self)
        self.__auth.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.__auth.setEnabled(False)
        layout.addWidget(self.__auth, 2, 2)

        self.__message_label = QLabel(self)
        _palette = QPalette()
        _palette.setColor(QPalette.WindowText, QColor("red"))
        self.__message_label.setPalette(_palette)
        self.__message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.__message_label, 3, 0, 1, 3)

        prev_button = QPushButton("Back", self)
        layout.addWidget(prev_button, 4, 0, 1, 3, Qt.AlignLeft)

        client_worker.failed_sending_phone.connect(self.__on_send_phone_failed)
        client_worker.failed_sending_code_and_password.connect(self.__on_send_code_and_password_failed)
        prev_button.clicked.connect(parent.re_create_client)
        client_worker.requesting_code.connect(self.__on_code_request)
        self.sending_phone.connect(client_worker.send_phone)
        self.__phone_button.clicked.connect(self.__send_phone)
        self.__change_phone_button.clicked.connect(self.__change_phone)
        self.__auth.clicked.connect(self.__finish_auth)
        self.sending_code_and_password.connect(client_worker.send_code_and_password)
        client_worker.auth_completed.connect(self.__auth_completed)

    @Slot(str)
    def __on_send_phone_failed(self, message):
        self.__message_label.setText(message)
        self.__phone_label.setEnabled(True)
        self.__phone_input.setEnabled(True)
        self.__phone_button.setEnabled(True)

    @Slot(str)
    def __on_send_code_and_password_failed(self, message):
        self.__message_label.setText(message)
        self.__code_label.setEnabled(True)
        self.__code_input.setEnabled(True)
        self.__change_phone_button.setEnabled(True)
        self.__password_label.setEnabled(True)
        self.__password_input.setEnabled(True)
        self.__auth.setEnabled(True)

    @Slot()
    def __send_phone(self):
        self.__phone_label.setEnabled(False)
        self.__phone_input.setEnabled(False)
        self.__phone_button.setEnabled(False)
        self.sending_phone.emit(self.__phone_input.text())

    @Slot()
    def __on_code_request(self):
        self.__phone_label.setEnabled(False)
        self.__phone_input.setEnabled(False)
        self.__phone_button.setEnabled(False)
        self.__code_label.setEnabled(True)
        self.__code_input.setEnabled(True)
        self.__change_phone_button.setEnabled(True)
        self.__password_label.setEnabled(True)
        self.__password_input.setEnabled(True)
        self.__auth.setEnabled(True)

    @Slot()
    def __change_phone(self):
        self.__phone_label.setEnabled(True)
        self.__phone_input.setEnabled(True)
        self.__phone_button.setEnabled(True)
        self.__code_label.setEnabled(False)
        self.__code_input.setEnabled(False)
        self.__change_phone_button.setEnabled(False)
        self.__password_label.setEnabled(False)
        self.__password_input.setEnabled(False)
        self.__auth.setEnabled(False)

    @Slot()
    def __finish_auth(self):
        self.__code_label.setEnabled(False)
        self.__code_input.setEnabled(False)
        self.__change_phone_button.setEnabled(False)
        self.__password_label.setEnabled(False)
        self.__password_input.setEnabled(False)
        self.__auth.setEnabled(False)
        self.sending_code_and_password.emit(self.__phone_input.text(), self.__code_input.text(), self.__password_input.text())

    @Slot()
    def __auth_completed(self) -> None:
        self.__code_input.setText("")
        self.__password_input.setText("")


class FruitFight2022GameInterface(QWidget):
    pass
