
import random
import numpy as np



class Maker_players:
    def __init__(self, cards4plaer, humans, robots, mincars4plaer, maxcars4plaer, minplaers, 
                 sizecoloda, startpole, get_human_name = False, print_out = True):
        self.MAX_PLAYERS = None
        self.CARDS_4PLAYER = cards4plaer
        self.humans = humans
        self.get_human_name = get_human_name
        self.robots = robots
        self.MINCARDS_4PLAER = mincars4plaer
        self.MAXCARDS_4PLAER = maxcars4plaer
        self.MIN_PLAYERS = minplaers
        self.QQUANTY_COLODA = sizecoloda
        self.START_pole = startpole
        self.PRINT_OUT = print_out

    def __call__(self):
        players, cards4plaer = self.make_players(self.get_human_name)
        return players, cards4plaer

    @property
    def opros(self):
        err_h = True
        err_r = True
        err_cards = True

        while err_cards:
            if not self.CARDS_4PLAYER:
                try:
                    self.CARDS_4PLAYER = int(input(f"Specify the number of cards dealt from {self.MINCARDS_4PLAER} to {self.MAXCARDS_4PLAER} inclusive: "))
                    if self.MINCARDS_4PLAER <= self.CARDS_4PLAYER <= self.MAXCARDS_4PLAER:
                        err_cards = False
                except ValueError:
                    print("Error, specify the number of cards")
            else:
                if isinstance(self.CARDS_4PLAYER, int):
                    err_cards = False
                else:
                    print("Error, specify the number of cards")
                    self.CARDS_4PLAYER = None

        self.MAX_PLAYERS = self.QQUANTY_COLODA // self.CARDS_4PLAYER

        while err_h and err_r:
            if self.PRINT_OUT:
               print(f"The number of participants (robots and humans) should be in total not less than {self.MIN_PLAYERS} and not more than {self.MAX_PLAYERS}")
            while err_h:
                if not self.humans and self.humans != 0:
                    try:
                        self.humans = int(input('Enter the number of human players: '))
                        err_h = False
                    except ValueError:
                        print("Error, specify the number of humans")
                else:
                    if isinstance(self.humans, int):
                        print(f'The number of humans is already set - {self.humans}')
                        err_h = False
                    else:
                        print("Error, specify the number of humans")
                        self.humans = None

            while err_r:
                if not self.robots and self.robots != 0:
                    try:
                        self.robots = int(input('Enter the number of robot players: '))
                        err_r = False
                    except ValueError:
                        print("Error, specify the number of robots")
                else:
                    if isinstance(self.robots, int):
                        print(f'The number of robots is already set - {self.robots}')
                        err_r = False
                    else:
                        print("Error, specify the number of robots")
                        self.robots = None


                if self.humans + self.robots > self.MAX_PLAYERS or self.humans + self.robots < self.MIN_PLAYERS:
                    print(f'Error, the total number of players specified is not in the range {self.MIN_PLAYERS} - {self.MAX_PLAYERS}')
                    err_h = True
                    err_r = True
                    if self.humans == 0 and self.robots == 0:
                        self.humans = None
                        self.robots = None

        return self.humans, self.robots, self.CARDS_4PLAYER

    def make_player(self, robot=True, number=0, get_human_name = False):
        player = self.START_pole.copy().astype(int)
        if robot:
            style = random.choice(('min', 'rand'))
            player.name = f'Robot_{number}({style})'
        else:
            if get_human_name:
               player.name = input('Enter the human player name: ').title()
            else:  player.name = f'Human_{number}'
        return player

    def make_players(self, get_human_name = False):

        hum, rob, cards4plaer = self.opros
        players = []

        if hum:
            for j in range(hum):
                if get_human_name:
                    if self.PRINT_OUT:  print(f'Player {j + 1}:')
                    players.append(self.make_player(robot=False, get_human_name = get_human_name))
                else:
                    players.append(self.make_player(robot=False, number=j + 1, get_human_name = get_human_name))
        if rob:
            for i in range(rob):
                players.append(self.make_player(number=i + 1))

        return players, cards4plaer


class Razdaza:
    def __init__(self, playcoloda, cards4plaer, poleigry, bitta, startcoloda, print_out = True):
        self.PLAY_coloda = playcoloda
        self.CARDS_4PLAYER = cards4plaer
        self.BITA = bitta
        self.POLE_IGRY = poleigry
        self.START_coloda = startcoloda
        self.PLAY = True
        self.PRINT_OUT = print_out

    def __call__(self, players):
        players, self.PLAY = self.razdacha_cards(players)
        return players, self.PLAY

    def perebor(self, df):
        qty_card = (df != 0).sum().sum()
        return qty_card >= self.CARDS_4PLAYER

    def random_card(self, vibor, value_card=0):
        vibor_ = vibor.to_numpy()
        idx, jdx = np.where(vibor_ > value_card)
        i = random.randint(0, len(idx) - 1)
        return vibor.index[idx[i]], vibor.columns[jdx[i]]

    def take_cards(self, player, take='full'):
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
        sum_data = np.zeros_like(data[0])
        for el in data:
            sum_data += el.to_numpy()

        tech_sum = (self.PLAY_coloda + self.BITA + self.POLE_IGRY).to_numpy()
        invariant = sum_data + tech_sum - self.START_coloda.to_numpy()
        if invariant.sum().sum() != 0:
            print('Error control invariant cards')
            print(invariant)
            self.PLAY = False

    def razdacha_cards(self, players):
        for i in range(len(players)):
            qty_card = (players[i] != 0).sum().sum()
            if self.PLAY_coloda.sum().sum() and qty_card < self.CARDS_4PLAYER:
                if self.PRINT_OUT: print(f'Dealing cards to {players[i].name}')
                else: print(f'\rDealing cards to {players[i].name}', end='')
                players[i] = self.take_cards(players[i])
            self.control_invariant(players)
        return players, self.PLAY
