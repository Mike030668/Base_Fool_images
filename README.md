Project based on previous version [Base_Fool](https://github.com/Mike030668/Base_Fool)

# Durak Card Game

This project implements the classic Russian card game "Durak" (Fool). The game involves multiple players, including human and robot players, playing against each other with a standard deck of cards. The objective of the game is to avoid being the last player with cards in hand. The last player with cards is called the "Durak".

## Features

- **Multiple Players:** The game supports both human and robot players.
- **Dynamic Gameplay:** Players can make moves or pass their turn. Robot players can choose moves randomly or based on the minimum card strategy.
- **Interactive Visualization:** The game state, including the cards in hand, on the field, and in the discard pile, is visualized using `matplotlib`.
- **Clear Instructions:** Prompts and instructions are provided to guide human players throughout the game.

<img src='images/Game.png' width='520'> 

## Getting Started

Check in [colab](https://colab.research.google.com/gist/Mike030668/499b9e371ff373658a1819719e12b80a/play_fool.ipynb)

### Prerequisites

- Python 3.7 or higher
- Required Python packages: `matplotlib`, `numpy`, `pandas`, `IPython`

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/durak-card-game.git
   cd durak-card-game

### SAMPLES OF GAMES
#### 2 robots on rules
<img src="images/game_play_2_robots.gif" alt="gif"  width="370"/> <img src="images/game_play_2_robots_1.gif" alt="gif"  width="370"/>

#### robot on rules and rand modle
<img src="images/game_play_randmodel_robot.gif" alt="gif"  width="370"/> <img src="images/game_play_randmodel_robot_2.gif" alt="gif"  width="370"/>

#### robot on rules and human
<img src="images/game_play_human_robot.gif" alt="gif"  width="570"/>

### SAMPLES OF RL TRAIN
[RL FOOL](https://github.com/Mike030668/MIPT_magistratura/tree/main/RL/FINAL/DZ_3)
