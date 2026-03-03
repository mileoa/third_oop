from abc import ABC, abstractmethod
from typing import Optional


class PlayingFieldATD(ABC):

    # Команды
    @abstractmethod
    def init(self) -> None:
        """
        Инициализация поля.
        Предусловие:  поле ранее не было инициализировано.
        Постусловие:  поле заполнено и на поле нет комбинаций.
        """

    @abstractmethod
    def fill_top_row(self) -> None:
        """
        Заполнить строку сверху.
        Предусловие:  в верхней строке хотя бы одна позиция не заполнена.
        Постусловие:  верхняя строка полностью заполнена элементами.
        """

    @abstractmethod
    def shift_elements_down(self) -> None:
        """
        Сместить элементы вниз.
        Предусловие:  на поле есть пустые места.
        Постусловие:  элементы, под которыми есть пустое место, смещены на 1 ячейку вниз.
        """

    @abstractmethod
    def swap_elements(self, pos1: tuple, pos2: tuple) -> None:
        """
        Поменять элементы местами.
        Предусловие:  позиции не выходят за границы поля;
                      позиции являются соседними по горизонтали или вертикали.
        Постусловие:  элементы поменяны местами.
        """

    @abstractmethod
    def delete_elements(self, positions: list) -> None:
        """
        Удалить элементы.
        Предусловие:  позиции не выходят за границы поля;
                      на каждой позиции есть элемент.
        Постусловие:  элементы удалены.
        """

    # Запросы

    @abstractmethod
    def get_init_status(self) -> int:
        """Получить статус инициализации поля."""

    @abstractmethod
    def get_fill_top_row_status(self) -> int:
        """Получить статус заполнения строки сверху."""

    @abstractmethod
    def get_shift_down_status(self) -> int:
        """Получить статус смещения элементов вниз."""

    @abstractmethod
    def get_swap_status(self) -> int:
        """Получить статус обмена элементов местами."""

    @abstractmethod
    def get_delete_status(self) -> int:
        """Получить статус удаления элементов."""

    @abstractmethod
    def has_possible_moves(self) -> bool:
        """Есть ли возможные ходы, приводящие к комбинации."""

    @abstractmethod
    def find_combination(self) -> Optional[list]:
        """Найти и вернуть первую найденную комбинацию."""

    @abstractmethod
    def find_special_bonus_affected_elements(self, bonus) -> list:
        """
        Найти элементы, которые будут удалены при применении специального бонуса.
        Предусловие:  специальный бонус существует.
        Постусловие:  возвращает список позиций элементов, которые будут удалены.
        """

    @abstractmethod
    def get_field(self) -> list:
        """Получить представление игрового поля в виде двухмерной матрицы."""


class StatisticATD(ABC):

    # Команды

    @abstractmethod
    def record_move(self, move) -> None:
        """
        Записать ход.
        Постусловие: ход записан в историю ходов.`
        """

    @abstractmethod
    def delete_last_move(self) -> None:
        """
        Удалить последний ход.
        Предусловие:  ранее были выполнены ходы.
        Постусловие:  ход стёрт из истории.
        """

    @abstractmethod
    def record_score_by_combination(self, combination: list) -> None:
        """
        Записать количество очков по комбинации.
        Постусловие: к ранее записанным очкам добавлено количество очков
                     в соответствии с переданной комбинацией.
        """

    @abstractmethod
    def clear(self) -> None:
        """
        Очистить статистику.
        Постусловие: статистика обнулена.
        """

    # Запросы

    @abstractmethod
    def get_move_count(self) -> int:
        """Вернуть количество ходов."""

    @abstractmethod
    def get_score(self) -> int:
        """Вернуть количество очков."""

    @abstractmethod
    def get_record_move_status(self) -> int:
        """Вернуть статус записи хода."""

    @abstractmethod
    def get_last_move(self):
        """Вернуть последний ход."""


class ConsoleATD(ABC):

    # Команды

    @abstractmethod
    def render(self, context: dict) -> None:
        """
        Отрисовать интерфейс.
        Постусловие: отрисован интерфейс пользователя по полученному контексту.
        """

    @abstractmethod
    def request_command(self) -> None:
        """
        Получить команду от игрока.
        Постусловие: игрок ввёл команду.
        """

    # Запросы

    @abstractmethod
    def get_input_command(self):
        """Получить введённую команду."""


class GameplayATD(ABC):

    # Команды

    @abstractmethod
    def execute_state_action(self) -> None:
        """
        Выполнить действие состояния.
        Постусловие: действие состояния выполнено.
        """

    @abstractmethod
    def set_state(self, state: "GameStateATD") -> None:
        """
        Установить состояние.
        Постусловие: установлено переданное состояние.
        """

    # Запросы

    @abstractmethod
    def get_execution_status(self) -> int:
        """Получить результат выполнения действия состояния."""


class GameStateATD(ABC):

    # Команды

    @abstractmethod
    def execute(self) -> None:
        """
        Выполнить действие состояния.
        Постусловие: действие состояния выполнено.
        """

    # Запросы

    @abstractmethod
    def get_execution_status(self) -> int:
        """Получить результат выполнения действия состояния."""


class PlayerATD(ABC):

    # Команды

    @abstractmethod
    def add_bonus(self, bonus) -> None:
        """
        Добавить специальный бонус для дальнейшего применения вручную.
        Предусловие:  специальный бонус существует.
        Постусловие:  специальный бонус сохранён для дальнейшего использования.
        """

    @abstractmethod
    def remove_bonus(self, bonus) -> None:
        """
        Удалить специальный бонус из бонусов для дальнейшего использования.
        Предусловие:  специальный бонус был добавлен ранее.
        Постусловие:  бонус недоступен для использования.
        """

    @abstractmethod
    def clear(self) -> None:
        """
        Очистить данные игрока.
        Постусловие: все данные игрока очищены.
        """

    # Запросы

    @abstractmethod
    def get_available_bonuses(self) -> list:
        """Получить список бонусов, доступных для дальнейшего использования."""

    @abstractmethod
    def has_bonus(self, bonus_type) -> bool:
        """Есть ли специальный бонус данного типа у игрока."""

    @abstractmethod
    def get_add_bonus_status(self) -> int:
        """Получить статус добавления бонуса."""

    @abstractmethod
    def get_remove_bonus_status(self) -> int:
        """Получить статус удаления бонуса."""
