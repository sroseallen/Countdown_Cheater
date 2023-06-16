# Countdown Numbers Game
A simple little command line game written in Python, with two modes modelled after the Countdown TV Numbers Game (made mostly to practise use of threading and recursive functions).

## Mode 1: Play the game

Initialise within your Python environment:

```python
from src.Countdown_Game import *
numbers_game()
```

The intructions should appear printed on the command line or within the environment, and will prompt entry of how many large numbers you want to play, as well as your answer. 

The function will also tell you what the closest number possible is, along with shorthand for the calculations to get there, after you enter your answer. Comes with a score tracker and the ability to play multiple rounds.

## Mode 2: Cheat

For people like me who also struggle with basic maths.

Initialise within your Python environment:

```python
from src.Countdown_Game import *
numbers_cheat()
```

Again instructions will appear and will prompt entry of the 6 numbers and the target number, and will then calculate the closest number and how to get there (in only a couple of seconds, well within the 30 second timer for the game).
