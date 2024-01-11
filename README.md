# Maze Game with Q-Learning Twin 🎮

Welcome to the Maze Game with Q-Learning Twin! This project combines a maze game with a Q-learning-based digital twin to provide hints for the player.

## Prerequisites

Before running the game, ensure you have Python and Pygame installed.

```bash
pip install pygame
```

## Getting Started
Run the Server

```
python server.py
```

Run the Maze Game
```
python Maze.py
```

Run the Digital Twin
```
python twin.py
```


## Gameplay
-  Navigate the maze using arrow keys in the maze.py game.
- Actions are twinned with the Q-learning model in twin.py.
- Q-learning suggests hints for the next action.

## Folder Structure
- maze.py: Maze game interface.
- twin.py: Q-learning twin for providing hints.
- server.py: Server handling communication.
