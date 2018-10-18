import random
from pynput.keyboard import Key, Listener

def on_press(key):

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


class card:
    def __init__(self, suit, value, face):
        self.suit = suit
        self.value = value
        self.face = face

    def __str__(self):
        return self.face + " of " + self.suit

    def __repr__(self):
        return self.face + " of " + self.suit

    def __gt__(self, other_card):
        return self.value > other_card.value

    def __lt__(self, other_card):
        return self.value < other_card.value

    def __eq__(self, other_card):
        return self.value == other_card.value


class deck:
    def __init__(self):

        self.suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        self.faces = ['Ace', '2', '3',
                      '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        self.values = [14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.deck = []

        for i in range(13):
            face = self.faces[i]
            value = self.values[i]
            for suit in self.suits:
                self.deck.append(card(suit, value, face))

    def __repr__(self):
        return self.deck

    def __str__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, index):
        result = self.deck[index]
        return result

    def __iter__(self, index):
        return self.deck[index]


def play_cards(table, deck):
    try:
        table.insert(0, deck.pop[0])
        print(table[0])
        if
        checkslap(table)
    except IndexError:
        print("Out of Cards!")


def cardslap(table):
    if table[0] == table[1]:
        # player takes cards
    elif table[0] == table[2]:
        # player takes cardS


unshuffled = deck()
gamedeck = []
for a_card in unshuffled[0:52]:
    gamedeck.append(a_card)
random.shuffle(gamedeck)
player1deck = []
player2deck = []
player3deck = []
player4deck = []
playdeck = []
while gamedeck:
    player1deck.append(gamedeck[0])
    gamedeck.pop(0)
    player2deck.append(gamedeck[0])
    gamedeck.pop(0)
    player3deck.append(gamedeck[0])
    gamedeck.pop(0)
    player4deck.append(gamedeck[0])
    gamedeck.pop(0)
face = False
while not face:
    for i in [1, 2, 3, 4]:
        if i == 1:
            print("Player 1 has played:")
            the_deck = player1deck
        elif i == 2:
            the_deck = player2deck
            print("Player 2 has played:")
        elif i == 3:
            the_deck = player3deck
            print("Player 3 has played:")
        elif == 4:
            the_deck = player4deck
            print("Player 4 has played:")
    playdeck = play_cards(playdeck, the_deck)