import random


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


def war(deck1, deck2, index):

    if len(deck1)- 1 >= index + 2:
        deck1_playedcard = deck1[index + 2]
    elif len(deck1)- 1 >= index + 1:
        deck1_playedcard = deck1[index + 1]
    else:
        return False, index
    if len(deck2)- 1 >= index + 2:
        deck2_playedcard = deck2[index + 2]
    elif len(deck2) - 1 >= index + 1:
        deck2_playedcard = deck2[index + 1]
    else:
        return True, index

    print("Your card: ", deck1_playedcard, ". Their card: ", deck2_playedcard)
    win = ""
    if deck1_playedcard > deck2_playedcard:
        print("War: You win!")
        win = True
    elif deck1_playedcard < deck2_playedcard:
        print("War: You lose!")
        win = False
    return win, index


unshuffled = deck()
gamedeck = []
for a_card in unshuffled[0:52]:
    gamedeck.append(a_card)
random.shuffle(gamedeck)
playerdeck = []
computerdeck = []

k, j = 0, 0
for i in range(len(gamedeck)):
    if i % 2 == 0:
        playerdeck.append(gamedeck[i])
        k += 1
    else:
        computerdeck.append(gamedeck[i])
        j += 1
        
cont  = False

while len(playerdeck) > 0 and len(computerdeck) > 0:
    if not cont:
        play = input("Play a card")
    
        if play == "card count":
            print(len(playerdeck))
        elif play == "continue":
            cont = True
        elif play == "peek":
            print(playerdeck[0])
        elif play == "peek 3":
            print(playerdeck[:3])

    player_card = playerdeck[0]
    computer_card = computerdeck[0]
    card_index = -2
    won = ""
    print("Your card: ", player_card, ". Their card: ", computer_card)
    if player_card == computer_card:
        while won == "":
            won, card_index = war(playerdeck, computerdeck, card_index + 3)
        if won :
            for a_card in range(card_index + 3):
                try:
                    playerdeck.append(playerdeck[0])
                    playerdeck.pop(0)
                    playerdeck.append(computerdeck[0])
                    computerdeck.pop(0)
                    print("You got card: ", playerdeck[-1])
                except IndexError:
                    pass
        else:
            for a_card in range(card_index + 3):
                try:
                    computerdeck.append(computerdeck[0])
                    computerdeck.pop(0)
                    computerdeck.append(playerdeck[0])
                    playerdeck.pop(0)
                    print("You lost card: ", computerdeck[-1])
                except IndexError:
                    pass
    elif player_card > computer_card:
        playerdeck.append(computer_card)
        computerdeck.pop(0)
        playerdeck.append(player_card)
        playerdeck.pop(0)
        print("You've won the round!")
    else:
        computerdeck.append(player_card)
        playerdeck.pop(0)
        computerdeck.append(computer_card)
        computerdeck.pop(0)
        print("You've lost the round")


if len(computerdeck) == 0:
    print("You've won the war!")
else:
    print("You've lost the war")

# input("press enter to continue")
