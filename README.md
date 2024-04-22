# sets-game
Sets game written in Python using pyglet library

### Game mechanic description

The deck consists of 81 cards varying in four features: 
* color: red, purple, green
* number: one, two, three
* shape: diamond, squiggle, oval
* pattern: solid, striped, outlined

Each possible combination of features (e.g., a card with three striped green diamonds) appears precisely once in the deck.

A set consists of three cards satisfying all of these conditions:
* They all have the same number or have three different numbers.
* They all have the same symbol or have three different symbols.
* They all have the same shading or have three different shadings.
* They all have the same color or have three different colors.

In the beginning of game player see 12 cards. Goal is to find all sets. 
If there are no any sets visible, player can request three more cards, 
with total of 15.

Scoring: +1 point to set found, -1 for wrong set clicked.

### Python implementation  

At current state game is finished and playable.

**In-game menu help**
```
  Game mode:
  Quickstart - 27 cards in game (3 features)
  Normal - 81 cards in game (4 features)

  Scoring:
  +1 point if found set is valid
  -1 point if found set is invalid

  Key shortcuts:
  G   - Display hint - number of sets
  H   - Display hint - two of three cards from set) 
  N   - Add 5th cards column (can be done only once)
  R   - Restart game
  F10 - Main menu
  ESC - Exit app
```

**Features**

* [Game] Normal and quickstart mode
* [Game] Hints: Add H key to automatically show two out of three cards from random set
* [Tech] Finite State Machine for three game states (menu, game, end) and transitions between them
* [Tech] Full mouse support


*Game Menu*

<img src="docs/game_menu.png" width="400" height="245" />

*Quickstart Mode*

<img src="docs/game_quickstart.png" width="400" height="245" />

*Normal Mode with 5th column*

<img src="docs/game_normal_fifth_column.png" width="400" height="245" />


---

### Development env

Python version: 3.11

```
pip install -r requirements.txt
```

### Run game

```
python run_game.py
```

### Build exe in Windows

```
pip install pyinstaller
pyinstaller .\run_game.spec
```


---

Reference:

* [Wikipedia - Set (card game)](https://en.wikipedia.org/wiki/Set_(card_game))
