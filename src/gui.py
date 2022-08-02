from PySide2.QtCore import QPoint, QRect, Qt, Signal, Slot
from PySide2.QtGui import QBrush, QColor, QFont, QFontMetrics, QLinearGradient, QPainter, QPalette, QPen, QTextOption
from PySide2.QtWidgets import QApplication, QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QRadioButton, QScrollBar, QSizePolicy, QToolButton, QVBoxLayout, QWidget

from game import Bone, GameState


class FruitFight2022MainWindow(QMainWindow):
    closed = Signal()

    def __init__(self, client_worker):
        super().__init__()
        self.__client_worker = client_worker
        self.setWindowTitle("ChatWars Fruit fight 2022 GUI Client")
        self.__client_config_tab = FruitFight2022ClientConfiguration(self, client_worker)
        self.__account_auth_tab = FruitFight2022AccountAuth(self, client_worker)
        self.__game_interface_tab = FruitFight2022GameInterface(self, client_worker)
        self.setCentralWidget(self.__client_config_tab)
        # self.setCentralWidget(self.__game_interface_tab)
        client_worker.client_created.connect(self.__on_client_created)
        client_worker.auth_completed.connect(self.__on_auth_completed)

    @Slot()
    def __on_client_created(self):
        self.setCentralWidget(self.__account_auth_tab)

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

        self.__create_client_button = QPushButton("Create client", self)
        layout.addWidget(self.__create_client_button, 6, 0, 1, 3, Qt.AlignRight)

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
        #
        # prev_button = QPushButton("Back", self)
        # layout.addWidget(prev_button, 4, 0, 1, 3, Qt.AlignLeft)

        client_worker.failed_sending_phone.connect(self.__on_send_phone_failed)
        client_worker.failed_sending_code_and_password.connect(self.__on_send_code_and_password_failed)
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
    def __init__(self, parent, client_worker):
        super().__init__(parent)
        layout = QGridLayout(self)
        self.setLayout(layout)

        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 2)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 0)

        self.__chats = FruitFight2022GameInterface.ChatsList(self)
        self.__chats.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.__chats, 0, 1)

        self.__game = FruitFight2022GameInterface.GamePanel(self)
        self.__game.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.__game, 0, 2, 2, 1)

        self.__chats_data = dict()
        self.__stamina_max_cache = dict()
        self.__current_chat = None

        client_worker.sending_state.connect(self.__on_chat_update)
        client_worker.chat_removing.connect(self.__on_chat_delete)
        self.__chats.selected.connect(self.__on_chat_select)
        self.__chats.unselected.connect(self.__on_chat_unselect)

    @Slot(object)
    def __on_chat_delete(self, cid):
        if cid not in self.__chats_data:
            return
        self.__chats_data.pop(cid)
        self.__chats.remove_cid(cid)
        self.__stamina_max_cache.pop(cid)

    @Slot(object, str, GameState)
    def __on_chat_update(self, cid, chat_name, data):
        self.__chats_data[cid] = data
        self.__stamina_max_cache[cid] = max(self.__stamina_max_cache.get(cid, 0), data.stamina)
        ci = FruitFight2022GameInterface.ChatItem(cid, chat_name)
        ci.players_count = len(data.players)
        self.__chats.ensure_chat(ci)
        if cid == self.__current_chat:
            self.__game.set_data(self.__chats_data[cid], self.__stamina_max_cache[cid])

    @Slot(object)
    def __on_chat_select(self, cid):
        if cid not in self.__chats_data:
            return
        self.__game.setEnabled(True)
        self.__game.set_data(self.__chats_data[cid], self.__stamina_max_cache[cid])
        self.__current_chat = cid

    @Slot()
    def __on_chat_unselect(self):
        self.__game.setEnabled(False)
        self.__current_chat = None

    class StaminaPanel(QWidget):
        def __init__(self, parent):
            super().__init__(parent)

            self.__label = QLabel(self)
            self.__bar = FruitFight2022GameInterface.StaminaHBar(self)
            self.__bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.set_left_max(0, 1)

            layout = QHBoxLayout(self)
            layout.addWidget(self.__label, 0)
            layout.addWidget(self.__bar, 1)

        def __update_label(self):
            self.__label.setText("Stamina: " + str(self.__left) + "/" + str(self.__max))

        def set_left_max(self, left, mx):
            self.__max = max(mx, 1)
            self.__left = max(0, left)
            self.__bar.set_left_max(left, mx)
            self.__update_label()

        def set_left(self, left) -> None:
            self.__left = max(0, left)
            self.__bar.set_left(left)
            self.__update_label()

    class StaminaHBar(QWidget):
        def __init__(self, parent):
            super().__init__(parent)

            self.setMinimumHeight(3)
            self.setMinimumWidth(3)

            self.__max = 1
            self.__left = 0

        def paintEvent(self, event) -> None:
            qp = QPainter(self)
            qp.setBrush(QBrush(QColor(0, 127, 0)))
            qp.setPen(QPen(QColor(0, 0, 0)))
            qp.drawRect(0, 0, self.width() - 1, self.height() - 1)
            qp.setBrush(QBrush(QColor(0, 255, 0)))
            qp.drawRect(0, 0, (self.width() - 1) * self.__left // self.__max, self.height() - 1)
            for i in range(1, self.__max):
                x = self.width() * i // self.__max
                qp.drawLine(x, 0, x, self.height() - 1)
            qp.end()

        def set_left_max(self, left, mx):
            self.__max = max(mx, 1)
            self.__left = max(0, left)
            self.repaint()

        def set_left(self, left) -> None:
            self.__left = max(0, left)
            self.repaint()

    class GamePanel(QWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.__stamina = FruitFight2022GameInterface.StaminaPanel(self)
            self.__hands = FruitFight2022GameInterface.PlayersHands(self)

            layout = QVBoxLayout(self)
            self.setLayout(layout)
            layout.addWidget(self.__stamina, 0)
            layout.addWidget(self.__hands, 0)
            layout.addStretch(1)

        def set_data(self, data, max_stamina: int):
            self.__stamina.set_left_max(data.stamina, max_stamina)
            self.__hands.ensure_players_count(len(data.players))
            for i, player in enumerate(data.players):
                self.__hands.set_row(i, player.is_turn, player.name, player.bones)

    class ChatItem:
        __slots__ = ("__cid", "__name", "__is_turn", "__players_count")

        def __init__(self, cid, name=""):

            self.__cid = cid
            self.__name = name
            self.__is_turn = False
            self.__players_count = 0

        @property
        def cid(self):
            return self.__cid

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, value):
            if type(value) is not str:
                raise TypeError("Chat name must be str")
            self.__name = value

        @property
        def is_turn(self):
            return self.__is_turn

        @is_turn.setter
        def is_turn(self, value):
            if type(value) is not bool:
                raise TypeError("Property 'is_turn' must be bool")
            self.__is_turn = value

        @property
        def players_count(self):
            return self.__players_count

        @players_count.setter
        def players_count(self, value):
            if type(value) is not int:
                raise TypeError("Player count must be int")
            if value <= 0:
                raise ValueError("Player count must be positive")
            self.__players_count = value

    class ChatsList(QWidget):
        selected = Signal(object)
        unselected = Signal()

        def __init__(self, parent):
            super().__init__(parent)

            layout = QHBoxLayout(self)
            self.setLayout(layout)

            self.__canvas = FruitFight2022GameInterface.ChatsList.Canvas(self, self.selected, self.unselected)
            self.__canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(self.__canvas, 1)

            self.__scrollbar = QScrollBar(self)
            self.__scrollbar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.__scrollbar.setMinimum(0)
            self.__scrollbar.setSingleStep(10)
            layout.addWidget(self.__scrollbar, 0)

            self.__canvas.scrolled.connect(self.__on_canvas_scroll)
            self.__scrollbar.valueChanged.connect(self.__canvas.on_bar_scroll)

        def move_cid_to_top(self, cid):
            self.__canvas.move_cid_to_top(cid)

        def remove_cid(self, cid):
            self.__canvas.remove_cid(cid)

        def ensure_chat(self, chat):
            self.__canvas.ensure_chat(chat)

        @Slot(int, int, int)
        def __on_canvas_scroll(self, size, page, y):
            self.__scrollbar.setMaximum(max(size, 0))
            self.__scrollbar.setPageStep(page)
            self.__scrollbar.setValue(y)

        class Canvas(QWidget):
            scrolled = Signal(int, int, int)

            @property
            def items_height(self):
                return self.__height * len(self.__data)

            def __init__(self, parent, selected_signal, unselected_signal):
                super().__init__(parent)

                self.__data = []
                self.__fheight = QFontMetrics(QFont().defaultFamily()).height()
                self.__height = self.__fheight + 6
                self.__y = 0
                self.__selected = None
                self.__selected_signal = selected_signal
                self.__unselected_signal = unselected_signal
                self.setMinimumWidth(50)
                self.setMinimumHeight(self.__height)

            def move_cid_to_top(self, cid):
                for i, wid in enumerate(self.__data):
                    if wid.cid == cid:
                        self.__data = [wid] + self.__data[:i] + self.__data[i + 1:]
                        if self.__selected < i:
                            self.__selected += 1
                        elif self.__selected == i:
                            self.__selected = 0
                        break
                else:
                    raise ValueError("Chat item with cid " + str(cid) + " not found")

                self.repaint()

            def paintEvent(self, event):
                i = self.__y // self.__height
                y = self.__height * i - self.__y
                qp = QPainter(self)
                while y < self.height():
                    if i >= len(self.__data):
                        break
                    self.__draw_item(qp, y, self.__data[i], self.__selected is not None and self.__selected == i)
                    y += self.__height
                    i += 1
                qp.end()

            def remove_cid(self, cid):
                for i, wid in enumerate(self.__data):
                    if wid.cid == cid:
                        self.__data.pop(i)
                        if self.__selected > i:
                            self.__selected -= 1
                        elif self.__selected == i:
                            self.__selected = None
                            self.__unselected_signal.emit()
                        break
                else:
                    raise ValueError("Chat item with cid " + str(cid) + " not found")

                self.repaint()

            def ensure_chat(self, chat):
                for wid in self.__data:
                    if wid.cid == chat.cid:
                        return
                self.__data.append(chat)
                self.repaint()
                self.__calc_scroll()

            def __draw_item(self, qp, y, data, is_selected):
                if data.is_turn:
                    background = QColor(100, 100, 255)
                else:
                    background = QColor(200, 200, 255)
                qp.setBrush(QBrush(background))
                qp.setPen(Qt.NoPen)
                qp.drawRect(0, y, self.width(), self.__height)
                qp.setPen(QPen(QColor(0, 0, 0)))
                margin = (self.__height - self.__fheight) // 2
                to = QTextOption(Qt.AlignVCenter)
                to.setWrapMode(QTextOption.NoWrap)
                qp.drawText(QRect(margin, y + margin, self.width(), self.__fheight), data.name, to)
                del to
                r = QRect(self.width() - 20 - 10 * data.players_count, y, 15, self.__height)
                gradient = QLinearGradient(r.bottomLeft(), r.topRight())
                gradient.setStart(r.bottomLeft())
                gradient.setFinalStop(r.bottomRight())
                gradient.setColorAt(0, QColor(background.red(), background.green(), background.blue(), 0))
                gradient.setColorAt(1, background)
                qp.fillRect(r, gradient)
                del r, gradient
                qp.fillRect(self.width() - 5 - 10 * data.players_count, y, 10 * data.players_count + 5, self.__height, background)
                qp.setBrush(QBrush(QColor(255, 255, 0)))
                point_h_center = self.__height // 2 + y
                for x in range(self.width() - 5, self.width() - 5 - 10 * data.players_count, -10):
                    qp.drawPolygon((QPoint(x - 4, point_h_center - 7), QPoint(x, point_h_center), QPoint(x - 4, point_h_center + 7), QPoint(x - 8, point_h_center)))
                del point_h_center
                if is_selected:
                    r = QRect(self.width() - 25, y, 25, self.__height)
                    gradient = QLinearGradient(r.bottomLeft(), r.topRight())
                    gradient.setStart(r.bottomLeft())
                    gradient.setFinalStop(r.bottomRight())
                    gradient.setColorAt(0, QColor(background.red(), background.green(), background.blue(), 0))
                    gradient.setColorAt(0.8, QColor(255, 0, 0))
                    gradient.setColorAt(1, QColor(255, 0, 0))
                    qp.fillRect(r, gradient)
                    del r, gradient
                qp.drawLine(0, y, self.width(), y)
                qp.drawLine(0, y + self.__height, self.width(), y + self.__height)

            def __calc_scroll(self):
                self.scrolled.emit(self.__height * len(self.__data) - self.height(), self.height(), self.__y)

            @Slot(int)
            def on_bar_scroll(self, y):
                self.__y = max(y, 0)
                self.repaint()

            def resizeEvent(self, event):
                self.__calc_scroll()

            def wheelEvent(self, event):
                self.__y = max(0, self.__y - event.angleDelta().y())
                self.__calc_scroll()

            def mousePressEvent(self, event):
                i = (event.y() + self.__y) // self.__height
                if i >= len(self.__data):
                    return

                self.__selected = i
                self.__selected_signal.emit(self.__data[i].cid)
                self.repaint()

    class BonesRow(QWidget):
        def __init__(self, parent):
            super().__init__(parent)

            self.__data = ()

            self.__calc_size(0)

        def resizeEvent(self, event):
            self.__calc_size(event.size().height())
            self.repaint()

        def __calc_size(self, height):
            self.setMinimumWidth(Bone.width(height) * len(self.__data) + len(self.__data) - 1)

        @Slot(tuple)
        def set_data(self, data) -> None:
            if type(data) is not tuple:
                raise TypeError("Bones row must be tuple")
            for bone in data:
                if type(bone) is not Bone:
                    raise TypeError("Bone has invalid type")
            self.__data = data

            self.__calc_size(self.height())
            self.repaint()

        def paintEvent(self, event):
            qp = QPainter(self)
            for i, bone in enumerate(self.__data):
                bone.paint(qp, Bone.width(self.height() - 1) * i + i * 2, 0, self.height() - 1)
            qp.end()

    class TurnPointer(QWidget):
        def __init__(self, parent):
            super().__init__(parent)

            self.__is_on = False

        def heightForWidth(self, width):
            return width

        def set(self, value):
            if type(value) is not bool:
                raise TypeError("State must be bool")
            self.__is_on = value

        def paintEvent(self, event):
            qp = QPainter(self)
            qp.setPen(QPen(QColor(0, 0, 0)))
            qp.setBrush(QBrush(QColor(0, 0, 255)))
            qp.drawEllipse(0, 0, self.width(), self.height())
            qp.end()

    class PlayersHands(QWidget):
        def __init__(self, parent):
            super().__init__(parent)

            self.__layout = QGridLayout(self)
            self.setLayout(self.__layout)
            self.__layout.setColumnStretch(0, 0)
            self.__layout.setColumnStretch(1, 0)
            self.__layout.setColumnStretch(2, 1)

            self.__pointers = []
            self.__names = []
            self.__hands = []

        def set_row(self, index, turn, name, hand):
            if index < 0 or index >= len(self.__hands):
                raise ValueError("Invalid row index")

            if turn:
                for pointer in self.__pointers:
                    pointer.set(False)
            self.__pointers[index].set(turn)
            self.__names[index].setText(name)
            self.__hands[index].set_data(hand)

        def ensure_players_count(self, count):
            while len(self.__hands) < count:
                pointer = FruitFight2022GameInterface.TurnPointer(self)
                self.__layout.addWidget(pointer, len(self.__pointers), 0)
                pointer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.__pointers.append(pointer)
                name = QLabel(self)
                self.__layout.addWidget(name, len(self.__names), 1, Qt.AlignLeft)
                self.__names.append(name)
                hand = FruitFight2022GameInterface.BonesRow(self)
                self.__layout.addWidget(hand, len(self.__hands), 2)
                hand.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.__hands.append(hand)
