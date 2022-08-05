from re import Pattern
from typing import ClassVar, List, NoReturn, Optional, Tuple, Union

from PySide2.QtGui import QPainter
from PySide2.QtSvg import QSvgRenderer
from telethon.tl.custom import MessageButton


class Cwff2022gcFruit:
    Apple: ClassVar[Cwff2022gcFruit] = ...
    Banana: ClassVar[Cwff2022gcFruit] = ...
    Cherry: ClassVar[Cwff2022gcFruit] = ...
    Lemon: ClassVar[Cwff2022gcFruit] = ...
    Orange: ClassVar[Cwff2022gcFruit] = ...
    Pineapple: ClassVar[Cwff2022gcFruit] = ...
    Watermelon: ClassVar[Cwff2022gcFruit] = ...

    __values__: ClassVar[Tuple[Cwff2022gcFruit, ...]] = ...

    emoji_regexp: ClassVar[Pattern] = ...

    @property
    def __name__(self) -> str: ...

    @property
    def emoji(self) -> str: ...

    @property
    def renderer(self) -> QSvgRenderer: ...

    @staticmethod
    def from_emoji(emoji) -> Cwff2022gcFruit: ...

    def __new__(cls, *args, **kwargs) -> NoReturn: ...


class Cwff2022gcBone:
    def __init__(self, left: Cwff2022gcFruit, right: Cwff2022gcFruit) -> None: ...

    @property
    def left(self) -> Cwff2022gcFruit: ...

    @property
    def right(self) -> Cwff2022gcFruit: ...

    @staticmethod
    def height_to_width(height: int) -> int: ...

    def paint(self, qp: QPainter, x: int, y: int, height: int) -> None: ...


class Cwff202gcButtonWithBone(Cwff2022gcBone):
    def __init__(self, left: Cwff2022gcFruit, right: Cwff2022gcFruit, button: MessageButton) -> None: ...

    @property
    def button(self) -> MessageButton: ...


class Cwff2022gcChatInfo:
    @classmethod
    def __new__(cls, cid: int, name: str) -> Cwff2022gcChatInfo: ...

    @property
    def cid(self) -> int: ...

    @property
    def name(self) -> str: ...

    @property
    def is_turn(self) -> bool: ...

    @is_turn.setter
    def is_turn(self, value: bool) -> None: ...

    @property
    def is_joinable(self) -> bool: ...

    @is_joinable.setter
    def is_joinable(self, value: bool) -> None: ...

    @property
    def is_started(self) -> bool: ...

    @is_started.setter
    def is_started(self, value: bool) -> None: ...

    @property
    def players_count(self) -> int: ...

    @players_count.setter
    def players_count(self, value: int) -> None: ...


class Cwff202gcSkipTurnButton:
    @classmethod
    def __new__(cls, button: MessageButton) -> Cwff202gcSkipTurnButton: ...

    @property
    def button(self) -> MessageButton: ...


class Cwff2022gcCollectingGame:
    @classmethod
    def __new__(
            cls,
            players: Tuple[str, ...],
            join_button: Optional[MessageButton],
            start_button: MessageButton
    ) -> Cwff2022gcCollectingGame: ...

    @property
    def players(self) -> Tuple[str, ...]: ...

    @property
    def join_button(self) -> Optional[MessageButton]: ...

    @property
    def start_button(self) -> MessageButton: ...


class Cwff2022gcGameState:
    @classmethod
    def __new__(
            cls,
            is_ended: bool,
            stamina: int,
            players: Tuple[Cwff2022gcPlayer],
            table: Cwff2022gcBone,
            buttons: Union[None, Cwff202gcSkipTurnButton, Tuple[Cwff202gcButtonWithBone, ...]]
    ) -> Cwff2022gcGameState: ...

    @property
    def is_ended(self) -> bool: ...

    @property
    def stamina(self) -> int: ...

    @property
    def players(self) -> Tuple[Cwff2022gcPlayer]: ...

    @property
    def table(self) -> Cwff2022gcBone: ...

    @property
    def buttons(self) -> Union[None, Cwff202gcSkipTurnButton, Tuple[Cwff202gcButtonWithBone, ...]]: ...


class Cwff2022gcPlayer:
    @classmethod
    def __new__(
            cls,
            is_turn: bool,
            name: str,
            bones: Tuple[MessageButton, ...]
    ) -> Cwff2022gcPlayer: ...

    @property
    def is_turn(self) -> bool: ...

    @property
    def name(self) -> str: ...

    @property
    def bones(self) -> Tuple[MessageButton, ...]: ...


def cwff2022gcParseGameMessage(raw_text: str, ibuttons: Optional[List[List[MessageButton]]]) -> Union[None, Cwff2022gcCollectingGame, Cwff2022gcGameState]: ...
