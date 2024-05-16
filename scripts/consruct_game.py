from scripts.elements_gane import Razdaza, Make_players

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image, display
import numpy as np
import pandas as pd
import random
import os

class Make_game:
    def __init__(self,
                 cards4player,
                 suits,
                 typecard_keys,
                 idx_suits,
                 idx_typecards,
                 startdeck,
                 img_path="images/"):
        self.CARDS_4PLAYER = cards4player
        self.SUITS = suits
        self.TYPECARD_KEYS = typecard_keys
        self.IDX_SUITS = idx_suits
        self.IDX_TYPECARDS = idx_typecards
        self.START_DECK = startdeck
        self.IMG_PATH = img_path
        self.START_FIELD = pd.DataFrame(np.zeros(startdeck.shape),
                                        index=startdeck.index,
                                        columns=startdeck.columns).astype(int)
        self.BITA = self.START_FIELD.copy().astype(int)
        self.GAME_FIELD = self.START_FIELD.copy().astype(int)
        self.BITA.name = 'Discard Pile'
        self.GAME_FIELD.name = 'Game Field'
        self.PLAY = True

    def __call__(self, players, playdeck, trump):
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

    def display_game_state(self, players, game_field, bita, playdeck, trump):
        """
        Displays the current state of the game using matplotlib.

        Parameters:
        players (list): List of players.
        game_field (DataFrame): Current game field.
        bita (DataFrame): Discard pile.
        playdeck (DataFrame): Current deck of cards.
        trump (str): Current trump suit.
        """
        fig, ax = plt.subplots(figsize=(14, 8))

        # Define the positions
        human_y = 0
        robot_y = 6
        game_field_y = 3
        deck_x = 8
        discard_x_start = 10
        card_width = 1.2
        card_height = 1.8

        def display_cards(cards, start_x, start_y, show_back=False):
            print(f"Displaying {len(cards)} cards at position ({start_x}, {start_y})")
            for i, card in enumerate(cards):
                card_file = os.path.join(self.IMG_PATH, "back.png" if show_back else f"{card[2]}.png")
                print(f"Loading card image from {card_file}")
                if os.path.exists(card_file):
                    img = mpimg.imread(card_file)
                    ax.imshow(img, extent=[start_x + i * card_width, start_x + (i + 1) * card_width, start_y, start_y + card_height])
                    print(f"Card image {card_file} added to plot at {[start_x + i * card_width, start_x + (i + 1) * card_width, start_y, start_y + card_height]}")
                else:
                    print(f"Image file {card_file} not found")

        # Display human player cards (bottom row)
        human_cards = self.show_cards(players[0], show=False)
        display_cards(human_cards, 0, human_y)

        # Display robot player cards (top row, face down)
        robot_cards = self.show_cards(players[1], show=False)
        display_cards(robot_cards, 0, robot_y, show_back=True)

        # Display game field (middle row)
        game_cards = self.show_cards(game_field, show=False)
        display_cards(game_cards, 0, game_field_y)

        # Display discard pile (middle row, to the right of the game field)
        bita_cards = self.show_cards(bita, show=False)
        display_cards(bita_cards, discard_x_start, game_field_y)

        # Display deck (middle row, to the right of the discard pile)
        deck_img_path = os.path.join(self.IMG_PATH, "back.png")
        print(f"Loading deck image from {deck_img_path}")
        if os.path.exists(deck_img_path):
            deck_img = mpimg.imread(deck_img_path)
            ax.imshow(deck_img, extent=[deck_x, deck_x + card_width, game_field_y, game_field_y + card_height])
            print(f"Deck image {deck_img_path} added to plot at {[deck_x, deck_x + card_width, game_field_y, game_field_y + card_height]}")
        else:
            print(f"Deck image file {deck_img_path} not found")

        # Display trump card (middle row, to the right of the deck)
        trump_img_path = os.path.join(self.IMG_PATH, f"{trump}.png")
        print(f"Loading trump image from {trump_img_path}")
        if os.path.exists(trump_img_path):
            trump_img = mpimg.imread(trump_img_path)
            ax.imshow(trump_img, extent=[deck_x + card_width, deck_x + 2 * card_width, game_field_y, game_field_y + card_height])
            print(f"Trump image {trump_img_path} added to plot at {[deck_x + card_width, deck_x + 2 * card_width, game_field_y, game_field_y + card_height]}")
        else:
            print(f"Trump image file {trump_img_path} not found")

        # Hide axes
        ax.axis('off')
        plt.show()

    def show_cards(self, player, show=True):
        """
        Converts player's DataFrame to a list of cards and displays images.

        Parameters:
        player (DataFrame): Player.
        show (bool): Show the cards to the player (default is True).

        Returns:
        list: List of player's cards.
        """
        matrix = np.array(player)
        for_choose = []
        for idx_m in range(matrix.shape[0]):
            for idx_t in range(matrix.shape[1]):
                if matrix[idx_m][idx_t] != 0:
                    card_name = f"{self.TYPECARD_KEYS[idx_t]}_{self.SUITS[idx_m]}"
                    card = [player.index[idx_m], player.columns[idx_t], card_name]
                    for_choose.append(card)
        
        if show:
            print(f'Your cards, {player.name}:')
            for card in for_choose:
                card_file = f"{self.IMG_PATH}/{card[2]}.png"
                display(Image(filename=card_file))

        return for_choose




    def random_card(self, vibor, value_card=0):
        vibor_ = vibor.to_numpy()
        idx, jdx = np.where(vibor_ > value_card)
        i = random.randint(0, len(idx) - 1)
        return vibor.index[idx[i]], vibor.columns[jdx[i]]

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

    def human_step(self, player, qty_card, value_card=0):
        attempt = min(2, qty_card)
        try_card = True
        vibor = self.vibor_card(player, value_card)
        schet = 1
        for_choose = self.show_cards(player)
        available = self.show_cards(vibor, False)

        while try_card and schet < attempt + 1:
            print(f'Player {player.name}, your move, you have {attempt - schet + 1} attempts left')
            step = input('Enter card number or space to skip: ')
            if step == ' ':
                try_card = False
                return step, step
            elif step == 'stop':
                print(f'Player {player.name} stopped the game')
                try_card = False
                self.PLAY = False
                return ' ', ' '
            else:
                try:
                    step = int(step)
                    if step in np.arange(1, qty_card + 1):
                        try_card = False
                    else:
                        schet += 1
                        print(f'{player.name}, you entered an invalid card number, please be more careful')
                except ValueError:
                    print(f'{player.name}, a card number or space to skip is required, please be more careful')
                    schet += 1

            if not try_card:
                if vibor.sum().sum() == 0:
                    print(f'{player.name}, unfortunately, you do not have a valid move')
                    return ' ', ' '
                else:
                    hod = for_choose[step - 1]
                    schet += 1
                    step_suit, step_typecards, _ = hod
                    if hod in available:
                        print(f'{player.name}, your move {step_suit} {step_typecards} is accepted')
                        try_card = False
                        return step_suit, step_typecards
                    else:
                        try_card = True
            else:
                pass
        print(f'{player.name}, you have used up your {attempt + 1} attempts')
        return ' ', ' '

    def random_step(self, player, value_card=0):
        vibor = self.vibor_card(player, value_card)
        style = player.name.split('(')[1][:-1]

        if vibor.sum().sum() == 0:
            return ' ', ' '
        else:
            if style == 'min':
                return self.min_card(vibor, value_card)
            if style == 'rand':
                return self.random_card(vibor, value_card)

    def min_card(self, vibor, value_card=0):
        vibor_ = vibor.to_numpy()
        mask = vibor_ > value_card
        v_min = vibor_[mask].min()

        idx, jdx = np.where(vibor_ == v_min)
        i, j = random.choice(np.c_[idx, jdx])
        return vibor.index[i], vibor.columns[j]

    def step_player(self, player, type_player='human'):
        qty_card = (player != 0).sum().sum()
        if type_player == 'human':
            print()
            print(f'Your move, {player.name}')
            m, t = self.human_step(player, qty_card)
            if m == ' ' and t == ' ':
                print(f'Player {player.name} skipped the move')
                return player
        if type_player == 'robot':
            m, t = self.random_step(player)

        print(f'{player.name} made a move {m}_{t}')
        idx_s = self.SUITS.index(m)
        idx_t = self.TYPECARD_KEYS.index(t)

        self.GAME_FIELD.iloc[idx_s, idx_t] = player.iloc[idx_s, idx_t]
        player.iloc[idx_s, idx_t] = 0
        return player

    def answer_player(self, player, type_player='human'):
        [a], [b] = np.where(self.GAME_FIELD.applymap(lambda x: x != 0))
        value_card = self.GAME_FIELD.iloc[a][b]
        qty_plcard = (player != 0).sum().sum()
        if type_player == 'robot':
            m, t = self.random_step(player, value_card)
        if type_player == 'human':
            print()
            print(f'On the field: {self.SUITS[a]} {self.TYPECARD_KEYS[b]}')
            m, t = self.human_step(player, qty_plcard, value_card)
        if m == ' ' and t == ' ':
            print(f'Player {player.name} takes the card and skips the move')
            player.iloc[a][b] = self.GAME_FIELD.iloc[a][b]
            self.GAME_FIELD.iloc[a][b] = 0
            state = False
        else:
            print(f'Player {player.name} responds with {m}_{t}')
            idx_s = self.SUITS.index(m)
            idx_t = self.TYPECARD_KEYS.index(t)
            self.BITA.iloc[idx_s, idx_t] = player.iloc[idx_s, idx_t]
            player.iloc[idx_s, idx_t] = 0
            self.BITA.iloc[a, b] = self.GAME_FIELD.iloc[a, b]
            self.GAME_FIELD.iloc[a][b] = 0
            state = True
        return player, state

    def action_player(self, player, state_player, type_action):
        type_player = self.get_type(player)
        if type_action:
            player = self.step_player(player, type_player)
            if not state_player[0]:
                state_player[0] = True
        else:
            player, state_player[0] = self.answer_player(player, type_player)
        state_player[1] = self.fin_play(player)
        return player, state_player

    def fin_play(self, player):
        set_player = player.sum().sum()
        set_deck = self.PLAY_DECK.sum().sum()
        if not set_player and not set_deck:
            print(f'Player {player.name} finished the game')
            return True
        else:
            return False

    def go_game(self, players, playdeck, trump):
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
            print('Cycle ', cycle)
            step = 0
            while step < qty_players and self.PLAY:
                if fin: fin += 1
                if self.GAME_FIELD.sum().sum() == 0:
                    type_action = True
                else:
                    type_action = False
                players[step], state_players[step] = self.action_player(players[step], state_players[step], type_action)
                razdacha_cards = Razdaza(self.PLAY_DECK, self.CARDS_4PLAYER, self.GAME_FIELD, self.BITA, self.START_DECK)
                if (players[step] != 0).sum().sum() < self.CARDS_4PLAYER:
                    players, self.PLAY = razdacha_cards(players)
                if sum(state_players[:, 1]) == 1:
                    fin += 1
                some_state = not type_action and not state_players[step][0]
                if type_action or some_state or state_players[step][1]:
                    step += 1
                if fin > 0: break
            if fin > 0:
                self.PLAY = False
                break
            cycle += 1
            print()

        print()
        winners = str()
        for player, state in zip(players, state_players):
            if state[1]: winners += player.name + ', '
        print(f'Victory for {winners[:-2]}')
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
    def __init__(self,
                 cards4player=None,
                 humans=None,
                 robots=None,
                 img_path="images/"):
        """
        Class for creating a "Durak" card game.
        
        Parameters:
        cards4player (int): Number of cards per player. Can be specified at initialization.
        humans (int): Number of human players. Can be specified at initialization.
        robots (int): Number of robot players. Can be specified at initialization.
        img_path (str): Path to the folder containing card images.
        """
        self.__humans = humans
        self.__robots = robots
        self.__CARDS_4PLAYER = cards4player
        self.__MUSTY = ['hearts', 'spades', 'clubs', 'diamonds']
        self.__DIC_CARDS = {'6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 11,
                            "queen": 12, 'king': 13, 'ace': 14}
        self.__TYPECARD_KEYS = list(self.__DIC_CARDS.keys())
        self.__IDX_MUSTY = np.arange(len(self.__MUSTY))
        self.__IDX_TYPECARDS = np.arange(len(self.__DIC_CARDS))
        self.__VALUE = [[card for card in self.__DIC_CARDS.values()] \
                        for i in range(len(self.__MUSTY))]
        self.__base_deck = pd.DataFrame(data=self.__VALUE,
                                        index=self.__MUSTY,
                                        columns=self.__DIC_CARDS.keys())
        self.__SHAPE = np.array(self.__base_deck).shape
        self.__DECK_SIZE = self.__SHAPE[0] * self.__SHAPE[1]
        self.__MAXCARDS_4PLAYER = int(np.sqrt(self.__DECK_SIZE))
        self.__START_FIELD = pd.DataFrame(np.zeros(self.__SHAPE),
                                          index=self.__MUSTY,
                                          columns=self.__DIC_CARDS.keys()).astype(int)
        self.__MINCARDS_4PLAYER = 2
        self.__MIN_PLAYERS = 2

        # Creation of the game launch method with current game values
        self.game_process = Make_game(self.__CARDS_4PLAYER,
                                      self.__MUSTY,
                                      self.__TYPECARD_KEYS,
                                      self.__IDX_MUSTY,
                                      self.__IDX_TYPECARDS,
                                      self.__base_deck,
                                      img_path)

    def init_game(self):
        """
        Function to initialize the game.
        """
        # Creation of the method to create players with current game values
        maker_players = Make_players(self.__CARDS_4PLAYER,
                                     self.__humans,
                                     self.__robots,
                                     self.__MINCARDS_4PLAYER,
                                     self.__MAXCARDS_4PLAYER,
                                     self.__MIN_PLAYERS,
                                     self.__DECK_SIZE,
                                     self.__START_FIELD)
        # Create players and update the number of cards to be dealt
        players, self.__CARDS_4PLAYER = maker_players()
        print()
        print("Randomly seating the players")
        random.shuffle(players)
        print([player.name for player in players])
        print("rand - robot with random choice of possible cards for the move")
        print("min - robot chooses the minimum possible card for the move ")
        print()

        print("Dealing cards:")
        # Update the game state
        trump = random.choice(self.__MUSTY)
        START_deck = self.__base_deck.copy().astype(int)
        START_deck.loc[trump] = START_deck.loc[trump] * 100
        PLAY_deck = START_deck.copy().astype(int)
        PLAY_deck.name = 'Game Deck'
        BITA = self.__START_FIELD.copy().astype(int)
        GAME_FIELD = self.__START_FIELD.copy().astype(int)

        # Create the method to deal cards with the current game values
        deal_cards = Razdaza(PLAY_deck,
                             self.__CARDS_4PLAYER,
                             GAME_FIELD,
                             BITA,
                             START_deck)

        # Deal cards to players
        players, play = deal_cards(players)
        print()
        print(f'Trump suit is {trump}')
        print()

        return players, PLAY_deck, trump
