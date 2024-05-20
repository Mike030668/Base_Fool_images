from scripts.elements_gane import Razdaza, Maker_players

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import clear_output
import numpy as np
import pandas as pd
import random
import os
import imageio
import PIL
import time

class Make_game:
    def __init__(self, cards4player, suits, typecard_keys, idx_suits, idx_typecards,
                 startdeck, img_path="images/", img_save_path="", make_gif = False,
                 print_out = True, plot_game = True):
        self.CARDS_4PLAYER = cards4player
        self.SUITS = suits
        self.TYPECARD_KEYS = typecard_keys
        self.IDX_SUITS = idx_suits
        self.IDX_TYPECARDS = idx_typecards
        self.START_DECK = startdeck
        self.IMG_PATH = img_path
        self.IMG_SAVE_PATH = img_save_path
        self.START_FIELD = pd.DataFrame(np.zeros(startdeck.shape), index=startdeck.index, columns=startdeck.columns).astype(int)
        self.BITA = self.START_FIELD.copy().astype(int)
        self.GAME_FIELD = self.START_FIELD.copy().astype(int)
        self.BITA.name = 'Discard Pile'
        self.GAME_FIELD.name = 'Game Field'
        self.PLAY = True
        self.PLAY_DECK = self.START_DECK.copy()
        self.TRUMP = None  # Initialize TRUMP
        self.frames = []  # To store frames for GIF
        self.MAKE_GIF = make_gif
        self.PRINT_OUT = print_out
        self.PLOT_GAME = plot_game

    def __call__(self, players, playdeck, trump):
        self.TRUMP = trump  # Set TRUMP when game starts
        self.go_game(players, playdeck, trump)

    def make_states(self, players):
        state_players = []
        for _ in range(len(players)):
            can_step = True
            fin_play = False
            state_players.append([can_step, fin_play])
        return np.array(state_players)

    def get_type(self, player):
        if player.name.split('_')[0].lower() == 'robot':
            return 'robot'
        else:
            return 'human'

    def display_game_state(self, players, game_field, bita, playdeck, trump, show=False, fig_size=(14, 8), gif_size = (920, 640)):

        def display_cards(cards, start_x, start_y, show_back=False):
            cards_per_row = 9
            for i, card in enumerate(cards):
                row = i // cards_per_row
                col = i % cards_per_row
                card_file = os.path.join(self.IMG_PATH, "back.png" if show_back else f"{card[2]}.png")
                if os.path.exists(card_file):
                    img = mpimg.imread(card_file)
                    ax.imshow(img, extent=[start_x + col * 1.2, start_x + (col + 1) * 1.2, start_y - row * 2, start_y - row * 2 + 1.8])
                else:
                    print(f"Image file {card_file} not found")
        self.fig_size = fig_size
        human_cards_y_start = 0.2
        robot_cards_y_start = 6

        human_cards = self.show_cards(players[0], show=show)
        y_add = 0
        # updaate
        if len(human_cards) > 9:
            y_add+=2
            human_cards_y_start += y_add
            robot_cards_y_start += y_add
            self.fig_size = (self.fig_size[0], self.fig_size[1] + y_add)

        robot_cards = self.show_cards(players[1], show=False)
        if len(robot_cards) > 9:
            y_add+=2
            human_cards_y_start += y_add
            robot_cards_y_start += y_add
            self.fig_size = (self.fig_size[0], self.fig_size[1] + y_add)

        fig, ax = plt.subplots(figsize = self.fig_size)
        ax.set_xlim(0, 12)
        ax.set_ylim(0, self.fig_size[1])  # Increased ylim to accommodate more cards
        ax.axis('off')

        y_centr = (self.fig_size[1] + y_add)/2 - 1

        display_cards(human_cards, 0, human_cards_y_start)  # Start human cards lowe
        display_cards(robot_cards, 0, robot_cards_y_start, show_back=True)  # Adjusted start_y for robot cards

        game_cards = self.show_cards(game_field, show=show)
        display_cards(game_cards, 3, y_centr) #3)

        deck_img_path = os.path.join(self.IMG_PATH, "back.png")
        play_desk = self.show_cards(self.PLAY_DECK, show=False)
        if len(play_desk):
            if os.path.exists(deck_img_path):
                deck_img = mpimg.imread(deck_img_path)
                ax.imshow(deck_img, extent=[8, 9.2, y_centr, y_centr + 1.8])
            else:
                print(f"Deck image file {deck_img_path} not found")

        trump_img_path = os.path.join(self.IMG_PATH, f"{trump}.png")
        if os.path.exists(trump_img_path):
            trump_img = mpimg.imread(trump_img_path)
            ax.imshow(trump_img, extent=[9.2, 10.4, y_centr, y_centr + 1.8])
        else:
            print(f"Trump image file {trump_img_path} not found")

        bita_cards = self.show_cards(bita, show=False)

        if len(bita_cards):
            if os.path.exists(deck_img_path):
                deck_img = mpimg.imread(deck_img_path)
                ax.imshow(deck_img, extent=[10.4, 11.6, y_centr, y_centr + 1.8])
            else:
                print(f"Deck image file {deck_img_path} not found")

        if self.PLOT_GAME:
            clear_output(True)
            plt.show()

        # Save frame for GIF
        if self.IMG_SAVE_PATH:
            fig.savefig(self.IMG_SAVE_PATH, bbox_inches='tight', pad_inches=0)   # save the figure to file
            plt.close(fig)    # close the figure window
        # Save frame for GIF
        if self.MAKE_GIF:
            frame = imageio.v2.imread(self.IMG_SAVE_PATH)
            frame = PIL.Image.fromarray(frame).resize(gif_size)
            self.frames.append(frame)

    def save_gif(self, gif_path="game_play.gif", duration=300):
        if self.MAKE_GIF:
            imageio.mimsave(gif_path, self.frames, duration=duration)
        else: pass

    def show_cards(self, player, show=True):
        matrix = np.array(player)
        for_choose = []
        for idx_m in range(matrix.shape[0]):
            for idx_t in range(matrix.shape[1]):
                if matrix[idx_m][idx_t] != 0:
                    card_name = f"{self.TYPECARD_KEYS[idx_t]}_{self.SUITS[idx_m]}"
                    card = [player.index[idx_m], player.columns[idx_t], card_name]
                    for_choose.append(card)
        return for_choose

    def vibor_card(self, df, value):
        if self.GAME_FIELD.sum().sum() == 0:
            vibor = df
        else:
            [a], [b] = np.where(self.GAME_FIELD.applymap(lambda x: x != 0))
            if self.SUITS[a] == self.TRUMP:
                vibor = df.apply(lambda x: x[x > value], 0).apply(lambda x: x[x > value], 1)
            else:
                vibor = df.loc[[self.SUITS[a], self.TRUMP]].apply(lambda x: x[x > value], 0).apply(lambda x: x[x > value], 1)
            vibor.replace(np.nan, 0, inplace=True)
        return vibor

    def human_step(self, player, qty_card, value_card, action_model):
        attempt = min(2, qty_card)
        try_card = True
        vibor = self.vibor_card(player, value_card)
        schet = 1
        for_choose = self.show_cards(player, False)
        available = self.show_cards(vibor, False)
        step_reward = 0
        if self.PRINT_OUT:
            if action_model != None:
                print(f"Used human model ")
            else:
                print(f"Human avswer")

        while try_card and schet < attempt + 1:

            if action_model == None:
                print(f'Player {player.name}, your move, you have {attempt - schet + 1} attempts left current reward {step_reward}')
                time.sleep(2)
                step = input('\nEnter card number or zero to skip: ')


            else:
                step =  action_model

            if step == 'stop':
                print(f'Player {player.name} stopped the game')
                try_card = False
                self.PLAY = False
                return 0, 0, step_reward
            else:
                try:
                    step = int(step)
                    if not step:
                        try_card = False
                        step_reward -= 1
                        return step, step, step_reward
                    elif step in np.arange(1, qty_card + 1):
                        try_card = False
                    else:
                        schet += 1
                        step_reward -= 1
                        if self.PRINT_OUT:
                            print(f'{player.name}, you entered an invalid card number, please be more careful, your step_reward {step_reward}')
                except ValueError:
                    print(f'{player.name}, a card number or space to skip is required, please be more careful')
                    schet += 1
                    step_reward -= 1


            if not try_card:
                if vibor.sum().sum() == 0:
                    step_reward -= 1
                    if self.PRINT_OUT:
                        print(f'{player.name}, unfortunately, you do not have a valid move')
                    return 0, 0, step_reward
                else:
                    hod = for_choose[step - 1]
                    schet += 1
                    step_suit, step_typecards = hod[0], hod[1]
                    available = [[av[0], av[1]] for av in available]

                    if [step_suit, step_typecards] in available:
                        if self.PRINT_OUT:
                            print(f'{player.name}, your move {step_suit} {step_typecards} is accepted, your step_reward {step_reward}')
                        try_card = False
                        return step_suit, step_typecards, step_reward
                    else:
                        try_card = True
                        step_reward -= 1
            else:
                pass

        return 0, 0, step_reward

    def random_step(self, player, value_card=0, step_reward = 0):
        vibor = self.vibor_card(player, value_card)
        style = player.name.split('(')[1][:-1]

        if vibor.sum().sum() == 0:
            return 0, 0, step_reward
        else:
            if style == 'min':
                m, t = self.min_card(vibor, value_card)

            if style == 'rand':
                m, t = self.min_card(vibor, value_card)
            return m, t, step_reward

    def min_card(self, vibor, value_card=0):
        vibor_ = vibor.to_numpy()
        mask = vibor_ > value_card
        v_min = vibor_[mask].min()

        idx, jdx = np.where(vibor_ == v_min)
        i, j = random.choice(np.c_[idx, jdx])
        return vibor.index[i], vibor.columns[j]

    def random_card(self, vibor, value_card=0):
        vibor_ = vibor.to_numpy()
        idx, jdx = np.where(vibor_ > value_card)
        i = random.randint(0, len(idx) - 1)
        return vibor.index[idx[i]], vibor.columns[jdx[i]]

    def step_player(self, player, type_player='human', action_model = None):
        qty_card = (player != 0).sum().sum()


        if type_player == 'human':
            if self.PRINT_OUT: print(f'Your move, {player.name}')
            else: print(f'\rYour move, {player.name}', end='')
            m, t, step_reward = self.human_step(player, qty_card, 0, action_model)
            if m == 0 and t == 0:
                if self.PRINT_OUT: print(f'Player {player.name} skipped the move')
                else: print(f'\rPlayer {player.name} skipped the move', end='')
                return player, step_reward

        if type_player == 'robot':
            m, t, step_reward = self.random_step(player)
        if self.PRINT_OUT: print(f'{player.name} made a move {m}_{t}')
        else: print(f'\r{player.name} made a move {m}_{t}', end='')
        idx_s = self.SUITS.index(m)
        idx_t = self.TYPECARD_KEYS.index(t)

        self.GAME_FIELD.iloc[idx_s, idx_t] = player.iloc[idx_s, idx_t]
        player.iloc[idx_s, idx_t] = 0
        return player, step_reward

    def answer_player(self, player, type_player='human', action_model = None):
        [a], [b] = np.where(self.GAME_FIELD.applymap(lambda x: x != 0))
        value_card = self.GAME_FIELD.iloc[a][b]
        qty_plcard = (player != 0).sum().sum()

        if type_player == 'robot':
            m, t, step_reward = self.random_step(player, value_card)

        if type_player == 'human':
            if self.PRINT_OUT:  print(f'\nOn the field: {self.SUITS[a]} {self.TYPECARD_KEYS[b]}')
            else: print(f'\rOn the field: {self.SUITS[a]} {self.TYPECARD_KEYS[b]}', end='')
            m, t, step_reward = self.human_step(player, qty_plcard, value_card, action_model)

        if m == 0 and t == 0:
            if self.PRINT_OUT: print(f'Player {player.name} takes the card and skips the move')
            else: print(f'\rPlayer {player.name} takes the card and skips the move', end='')
            player.iloc[a][b] = self.GAME_FIELD.iloc[a][b]
            self.GAME_FIELD.iloc[a][b] = 0
            state = False
        else:
            if self.PRINT_OUT:  print(f'Player {player.name} responds with {m}_{t}')
            else: print(f'\rPlayer {player.name} responds with {m}_{t}', end='')

            idx_s = self.SUITS.index(m)
            idx_t = self.TYPECARD_KEYS.index(t)
            self.BITA.iloc[idx_s, idx_t] = player.iloc[idx_s, idx_t]
            player.iloc[idx_s, idx_t] = 0
            self.BITA.iloc[a, b] = self.GAME_FIELD.iloc[a, b]
            self.GAME_FIELD.iloc[a][b] = 0
            state = True

        return player, state, step_reward

    def action_player(self, player, state_player, type_action, action_model = None):
        type_player = self.get_type(player)
        if type_action:
            player, step_reward  = self.step_player(player, type_player, action_model)
            if not state_player[0]:
                state_player[0] = True
        else:
            player, state_player[0], step_reward = self.answer_player(player, type_player, action_model)
        state_player[1] = self.fin_play(player)
        return player, state_player, step_reward

    def fin_play(self, player):
        set_player = player.sum().sum()
        set_deck = self.PLAY_DECK.sum().sum()
        if not set_player and not set_deck:
            print(f'\nPlayer {player.name} finished the game')
            return True
        else:
            return False

    def go_game(self, players, playdeck, trump, model = None):
        qty_players = len(players)
        self.CARDS_4PLAYER = (players[0] != 0).sum().sum()
        cycle = 1
        fin = 0
        self.PLAY = True
        self.TRUMP = trump
        self.PLAY_DECK = playdeck
        self.START_DECK.loc[self.TRUMP] *= 100

        df_list = [self.BITA, self.PLAY_DECK, self.GAME_FIELD]
        state_players = self.make_states(players)

        while self.PLAY:
            if self.PRINT_OUT:  print('Cycle ', cycle)
            step = 0
            while step < qty_players and self.PLAY:
                if fin: fin += 1
                if self.GAME_FIELD.sum().sum() == 0:
                    type_action = True
                else:
                    type_action = False
                if self.PRINT_OUT: print()
                self.display_game_state(players, self.GAME_FIELD, self.BITA, self.PLAY_DECK, self.TRUMP)

                if  self.get_type(players[step]) =="human" and model != None:
                    action_model = model()

                else:
                    action_model = None

                players[step], state_players[step], player_step_reward = self.action_player(players[step], state_players[step], type_action, action_model)
                razdacha_cards = Razdaza(self.PLAY_DECK, self.CARDS_4PLAYER, self.GAME_FIELD, self.BITA, self.START_DECK, self.PRINT_OUT)

                if (players[step] != 0).sum().sum() < self.CARDS_4PLAYER:
                    players, self.PLAY = razdacha_cards(players)
                if sum(state_players[:, 1]) == 1:
                    fin += 1

                some_state = not type_action and not state_players[step][0]
                if type_action or some_state or state_players[step][1]:
                    step += 1
                if fin > 0:
                  self.display_game_state(players, self.GAME_FIELD, self.BITA, self.PLAY_DECK, self.TRUMP)
                  break
            if fin > 0:
                self.PLAY = False
                break
            cycle += 1
            if self.PRINT_OUT: print()

        if self.PRINT_OUT: print()
        winners = str()
        for player, state in zip(players, state_players):
            if state[1]: winners += player.name + ', '
        print(f'\nVictory for {winners[:-2]}')
        print()

        print('Checking cards')
        for player in players:
            print(player.name)
            print(player.head(10).to_string())
            print()

        print('Checking other fields')
        for df in df_list:
            print(df.name)
            print(df.head(10).to_string())
            print()



class Durack:
    def __init__(self, cards4player=None, humans=1, robots=1, img_path="images/",
                 img_save_path = "", make_gif = False, print_out = True, plot_game = True, 
                 get_human_name = False):
        self.__humans = humans
        self.__robots = robots
        self.__CARDS_4PLAYER = cards4player
        self.__MUSTY = ['hearts', 'spades', 'clubs', 'diamonds']
        self.__DIC_CARDS = {'6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 11, "queen": 12, 'king': 13, 'ace': 14}
        self.__TYPECARD_KEYS = list(self.__DIC_CARDS.keys())
        self.__IDX_MUSTY = np.arange(len(self.__MUSTY))
        self.__IDX_TYPECARDS = np.arange(len(self.__DIC_CARDS))
        self.__VALUE = [[card for card in self.__DIC_CARDS.values()] for i in range(len(self.__MUSTY))]
        self.__base_deck = pd.DataFrame(data=self.__VALUE, index=self.__MUSTY, columns=self.__DIC_CARDS.keys())
        self.__SHAPE = np.array(self.__base_deck).shape
        self.__DECK_SIZE = self.__SHAPE[0] * self.__SHAPE[1]
        self.__MAXCARDS_4PLAYER = int(np.sqrt(self.__DECK_SIZE))
        self.__START_FIELD = pd.DataFrame(np.zeros(self.__SHAPE), index=self.__MUSTY, columns=self.__DIC_CARDS.keys()).astype(int)
        self.__MINCARDS_4PLAYER = 2
        self.__MIN_PLAYERS = 2
        self.img_save_path = img_save_path
        self.PRINT_OUT = print_out
        self.PLOT_GAME = plot_game
        self.get_human_name = get_human_name
        

        self.game_process = Make_game(self.__CARDS_4PLAYER, self.__MUSTY, self.__TYPECARD_KEYS,
                                      self.__IDX_MUSTY, self.__IDX_TYPECARDS, self.__base_deck,
                                      img_path, img_save_path, make_gif, print_out, plot_game)

    def init_game(self):
        maker_players = Maker_players(self.__CARDS_4PLAYER, self.__humans, self.__robots,
                                     self.__MINCARDS_4PLAYER, self.__MAXCARDS_4PLAYER,
                                     self.__MIN_PLAYERS, self.__DECK_SIZE, self.__START_FIELD,
                                     self.get_human_name,
                                     self.PRINT_OUT)

        players, self.__CARDS_4PLAYER = maker_players()
        if self.PRINT_OUT:
            print()
            print([player.name for player in players])
            print("rand - robot with random choice of possible cards for the move")
            print("min - robot chooses the minimum possible card for the move \n")
            print("Dealing cards:")

        trump = random.choice(self.__MUSTY)
        START_deck = self.__base_deck.copy().astype(int)
        START_deck.loc[trump] = START_deck.loc[trump] * 100
        PLAY_deck = START_deck.copy().astype(int)
        PLAY_deck.name = 'Game Deck'
        BITA = self.__START_FIELD.copy().astype(int)
        GAME_FIELD = self.__START_FIELD.copy().astype(int)

        deal_cards = Razdaza(PLAY_deck, self.__CARDS_4PLAYER, GAME_FIELD, BITA, START_deck, self.PRINT_OUT)

        players, play = deal_cards(players)
        if self.PRINT_OUT: print(f'\nTrump suit is {trump}\n')
        else: print(f'\rTrump suit is {trump}', end='')


        return players, PLAY_deck, trump