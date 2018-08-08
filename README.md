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

Scoring: +3 point to set found, -1 for wrong set clicked.

### Python implementation  

**TODO**

* [x] Display number of cards left in unused deck 
* [x] Replace old cards with fresh from unused deck when user finds correct set
* [x] Display menu in the beginning with features choice option (quickstart and complete option)
* [ ] Add penalty for clicking wrong cards that will decrease score
* [x] Display end game screen
* [ ] Add hints
    * Show how many sets are visible
    * Add button to automatically click random card from correct set 


---

Reference:

* [Wikipedia - Set (card game)](https://en.wikipedia.org/wiki/Set_(card_game))
