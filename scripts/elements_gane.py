
import random
import numpy as np


class Make_players:
    def __init__(self,
                 cards4plaer,
                 humans,
                 robots,
                 mincars4plaer,
                 maxcars4plaer,
                 minplaers,
                 sizecoloda,
                 startpole):
        """
        Класс для создания игроков в игре "Дурак".

        Параметры:
        cards4plaer (int): Количество карт для каждого игрока.
        humans (int): Количество людей-игроков.
        robots (int): Количество роботов-игроков.
        mincars4plaer (int): Минимальное количество карт для игрока.
        maxcars4plaer (int): Максимальное количество карт для игрока.
        minplaers (int): Минимальное количество игроков.
        sizecoloda (int): Размер колоды.
        startpole (DataFrame): Начальное игровое поле.
        """
        self.MAX_PLAYERS = None
        self.CARDS_4PLAYER = cards4plaer
        self.humans = humans
        self.robots = robots
        self.MINCARDS_4PLAER = mincars4plaer
        self.MAXCARDS_4PLAER = maxcars4plaer
        self.MIN_PLAYERS = minplaers
        self.QQUANTY_COLODA = sizecoloda
        self.START_pole = startpole

    def __call__(self):
        players, cards4plaer = self.maker_players()
        return players, cards4plaer

    @property
    def opros(self):
        """
        Функция опроса для установления параметров игры:
        CARDS_4PLAYER - количество карт у игроков.
        humans - количество людей в игре.
        robots - количество роботов в игре.
        """
        err_h = True
        err_r = True
        err_cards = True

        # Определение CARDS_4PLAYER
        while err_cards:
            if not self.CARDS_4PLAYER:
                try:
                    self.CARDS_4PLAYER = int(input(
                        f"Укажите количество карт выдаваемых на руки от {self.MINCARDS_4PLAER} до {self.MAXCARDS_4PLAER} включительно: "))
                    if self.MINCARDS_4PLAER <= self.CARDS_4PLAYER <= self.MAXCARDS_4PLAER:
                        err_cards = False
                except ValueError:
                    print("Ошибка, укажите число карт")
            else:
                if isinstance(self.CARDS_4PLAYER, int):
                    err_cards = False
                else:
                    print("Ошибка, укажите число карт")
                    self.CARDS_4PLAYER = None

        # Определение MAX_PLAYERS
        self.MAX_PLAYERS = self.QQUANTY_COLODA // self.CARDS_4PLAYER

        # Определение количества игроков (людей и роботов)
        while err_h and err_r:
            print(
                f"Количество участников (роботы и люди) должно быть в сумме не менее {self.MIN_PLAYERS} и не более {self.MAX_PLAYERS}")
            while err_h:
                if not self.humans and self.humans != 0:
                    try:
                        self.humans = int(input('Введите количество игроков людей: '))
                        err_h = False
                    except ValueError:
                        print("Ошибка, укажите число человек")
                else:
                    if isinstance(self.humans, int):
                        print(f'Количество людей уже задано - {self.humans}')
                        err_h = False
                    else:
                        print("Ошибка, укажите число человек")
                        self.humans = None

            while err_r:
                if not self.robots and self.robots != 0:
                    try:
                        self.robots = int(input('Введите количество игроков роботов: '))
                        err_r = False
                    except ValueError:
                        print("Ошибка, укажите число роботов")
                else:
                    if isinstance(self.robots, int):
                        print(f'Количество роботов уже задано - {self.robots}')
                        err_r = False
                    else:
                        print("Ошибка, укажите число роботов")
                        self.robots = None

                if self.humans + self.robots > self.MAX_PLAYERS \
                        or self.humans + self.robots < self.MIN_PLAYERS:
                    print(
                        f'Ошибка, указано суммарное количество игроков не в диапазоне {self.MIN_PLAYERS} - {self.MAX_PLAYERS}')
                    err_h = True
                    err_r = True
                    if self.humans == 0 and self.robots == 0:
                        self.humans = None
                        self.robots = None

        return self.humans, self.robots, self.CARDS_4PLAYER

    def make_player(self, robot=True, number=0):
        """
        Создает игрока.

        Параметры:
        robot (bool): Указывает, является ли игрок роботом.
        number (int): Порядковый номер робота.

        Возвращает:
        DataFrame: Игрок с присвоенным именем.
        """
        player = self.START_pole.copy().astype(int)
        if robot:
            style = random.choice(('min', 'rand'))
            player.name = f'Robot_{number}({style})'
        else:
            player.name = input('Введите имя человека: ').title()
        return player

    def maker_players(self):
        """
        Создает список игроков.

        Возвращает:
        list: Список игроков.
        int: Количество карт для каждого игрока.
        """
        hum, rob, cards4plaer = self.opros
        players = []
        if rob:
            for i in range(rob):
                players.append(self.make_player(number=i + 1))
        if hum:
            for _ in range(hum):
                print(f'Игрок {_ + 1}:')
                players.append(self.make_player(robot=False))
        return players, cards4plaer

class Razdaza:
    def __init__(self,
                 playcoloda,
                 cards4plaer,
                 poleigry,
                 bitta,
                 startcoloda):
        """
        Класс для раздачи карт игрокам.

        Параметры:
        playcoloda (DataFrame): Игровая колода.
        cards4plaer (int): Количество карт для каждого игрока.
        poleigry (DataFrame): Игровое поле.
        bitta (DataFrame): Бита.
        startcoloda (DataFrame): Начальная колода.
        """
        self.PLAY_coloda = playcoloda
        self.CARDS_4PLAYER = cards4plaer
        self.BITA = bitta
        self.POLE_IGRY = poleigry
        self.START_coloda = startcoloda
        self.PLAY = True

    def __call__(self, players):
        players, self.PLAY = self.razdacha_cards(players)
        return players, self.PLAY

    def perebor(self, df):
        """
        Контроль количества карт у игрока.

        Параметры:
        df (DataFrame): Карты игрока.

        Возвращает:
        bool: True, если у игрока достаточно карт, иначе False.
        """
        qty_card = (df != 0).sum().sum()
        return qty_card >= self.CARDS_4PLAYER

    def random_card(self, vibor, value_card=0):
        """
        Определяет случайный выбор карты из доступных.

        Параметры:
        vibor (DataFrame): Доступные карты.
        value_card (int): Значение карты.

        Возвращает:
        tuple: Масть и ранг выбранной карты.
        """
        vibor_ = vibor.to_numpy()
        idx, jdx = np.where(vibor_ > value_card)
        i = random.randint(0, len(idx) - 1)
        return vibor.index[idx[i]], vibor.columns[jdx[i]]

    def take_cards(self, player, take='full'):
        """
        Выдача карт из колоды игроку.

        Параметры:
        player (DataFrame): Игрок, которому выдаются карты.
        take (str or int): Сколько карт брать (по умолчанию до CARDS_4PLAYER).

        Возвращает:
        DataFrame: Игрок с обновленными картами.
        """
        take_card = True
        schet = 0

        while take_card:
            if self.perebor(player):
                take_card = False
            else:
                m, t = self.random_card(self.PLAY_coloda)
                idx_m = self.PLAY_coloda.index.tolist().index(m)
                idx_t = self.PLAY_coloda.columns.tolist().index(t)
                player.iloc[idx_m, idx_t] = self.PLAY_coloda.iloc[idx_m, idx_t]
                self.PLAY_coloda.iloc[idx_m, idx_t] = 0

                if not self.PLAY_coloda.sum().sum():
                    take_card = False

                schet += 1
                if take != 'full' and schet == take:
                    take_card = False

        return player

    def control_invariant(self, data):
        """
        Проверка инварианта игрового пространства для контроля игры.

        Параметры:
        data (list): Список DataFrame с данными игры.
        """
        sum_data = np.zeros_like(data[0])
        for el in data:
            sum_data += el.to_numpy()

        tech_sum = (self.PLAY_coloda + self.BITA + self.POLE_IGRY).to_numpy()
        invariant = sum_data + tech_sum - self.START_coloda.to_numpy()
        if invariant.sum().sum() != 0:
            print('Ошибка контроля invariant карт')
            print(invariant)
            self.PLAY = False

    def razdacha_cards(self, players):
        """
        Раздача карт игрокам.

        Параметры:
        players (list): Список игроков.

        Возвращает:
        list: Обновленный список игроков.
        bool: Статус игры (продолжается или закончена).
        """
        for i in range(len(players)):
            qty_card = (players[i] != 0).sum().sum()
            if self.PLAY_coloda.sum().sum() and qty_card < self.CARDS_4PLAYER:
                print(f'Выдача карт {players[i].name}')
                players[i] = self.take_cards(players[i])
            self.control_invariant(players)
        return players, self.PLAY
