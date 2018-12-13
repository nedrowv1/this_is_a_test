import random
import pygame
from pygame.locals import *
import sys
import Grandmas_Game_Closet as Main

RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (20, 100, 20)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
NAVY = (60, 60, 100)
DARKGREY = (30, 30, 30)
BLACK = (0, 0, 0)
TAN = (222, 184, 135)
ORANGE = (255, 128, 0)
LIGHTSKIN = (249, 222, 147)
WINWIDTH = 640
WINHEIGHT = 480

IMAGES = {}


class Card(object):
    """A single card, used in a deck
    attributes: suit, value, face"""

    def __init__(self, suit, value, face):
        """create a card of a given suit, value and face; when
        used with is_empty in a deck can be used to pre-set the deck"""
        self.suit = suit
        self.value = value
        self.face = face
        self.image = self.facelookup()

    def __str__(self):
        """print string of card"""
        return self.face + " of " + self.suit

    def __repr__(self):
        """save string of card"""
        return self.face + " of " + self.suit

    def __gt__(self, other_card):
        """compare cards"""
        try:
            return self.value > other_card.value
        except AttributeError:
            return False

    def __lt__(self, other_card):
        """compare cards"""
        try:
            return self.value < other_card.value
        except AttributeError:
            return False

    def __eq__(self, other_card):
        """compare cards; if other not a card, cannot be equal"""
        try:
            return self.value == other_card.value
        except AttributeError:
            return False
        
    def facelookup(self):
        """added for pygame integration, added card .png to object"""
        try:
            return IMAGES[self.face + self.suit]
        except KeyError:
            return IMAGES[self.face[0] + self.suit]


class Deck(object):
    """a deck of cards, also containing the dealt hands of the deck
    attributes: deck, hands"""

    def __init__(self, num_players=0, is_shuffled=False, is_empty=False):
        """num_players determines the number of hands to deal.
        zero default creates central card pool of 52 cards, 1 creates
        a single player deck of 52if is_shuffled is set to True, the saved
        deck will be already shuffled,if set to false, the deck will have
        to be shuffled manually if is_empty is set to True, an empty deck
        class will be created"""

        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        faces = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9',
                 '10', 'Jack', 'Queen', 'King']
        values = [14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.deck = []
        self.hands = []
        if not is_empty:
            for i in range(13):
                face = faces[i]
                value = values[i]
                for suit in suits:
                    self.deck.append(Card(suit, value, face))

            if is_shuffled:
                self.shuffle()

            if num_players > 1:
                self.deal(num_players)

    def __repr__(self):
        """save string of deck"""
        return self.deck

    def __str__(self):
        """print string of deck"""
        return str(self.deck)

    def __len__(self):
        """return length of deck"""
        return len(self.deck)

    def __getitem__(self, index):
        """make deck indexable"""
        return self.deck[index]

    def __iter__(self, index):
        """make deck iterable"""
        return self.deck[index]

    def shuffle(self):
        """shuffle self.deck"""
        return random.shuffle(self.deck)

    def deal(self, decks):
        """deal deck to player hands"""
        last_dealt = 0
        for a_player in range(decks):
            self.hands.append(Deck(is_empty=True))
        while len(self.deck) >= len(self.hands):
            for a_deck in range(len(self.hands)):
                self.hands[a_deck].deck.append(self.deck.pop(0))
                last_dealt = a_deck
        for a_card in range(len(self.deck)):
            self.hands[last_dealt].deck.append(self.deck.pop(0))
            last_dealt += 1

    def card(self):
        """return to top card of the deck"""
        return self.deck[0]

    def return_hands(self):
        """return the hands in the deck"""
        return self.hands

    def give_card(self, otherdeck):
        """give card from self deck to another deck, used for decks
        in self.hands"""
        otherdeck.deck.append(self.deck.pop(0))

    def move_card(self):
        """move top card in deck to the bottom,
        used for decks in self.hands"""
        self.deck.append(self.deck.pop(0))


def loadimages():
    """look up the objects image"""
    global IMAGES
    suits = ("Hearts", "Diamonds", "Spades", "Clubs")
    faces = ("2", "3", "4", "5", "6", "7", "8", "9", "10",
             "J", "Q", "K", "A")
    for suit in suits:
        for face in faces:
            image = "/" + face + "_of_" + suit.lower() + ".png"
            IMAGES[face + suit] = pygame.image.load('cards' + image)


def reset_war_globals(screen):
    """reset all the global variables used"""
    global FPS, fps_clock

    FPS = 60
    bg_color = DARKGREEN
    fps_clock = pygame.time.Clock()
    screen.fill(bg_color)
    loadimages()


def play_war(player, computer, screen, stop):
    """main game logic"""
    card_index = -2
    screen.blit(pygame.transform.scale(player.card().image, CARDSIZE),
                PLAYEDCARD_P)
    screen.blit(pygame.transform.scale(computer.card().image, CARDSIZE),
                PLAYEDCARD_C)
    if player.card() == computer.card():
        declare_war(player, computer, card_index + 3, screen)
        stop = True
    elif player.card() > computer.card():
        player.move_card()
        computer.give_card(player)
    else:
        computer.move_card()
        player.give_card(computer)
    return stop


def clear_screen(player, computer, screen):
    """clear played war cards from table"""
    if WIN:
        deck = player
        cov1 = COVERED_CARD1_P
        cov2 = COVERED_CARD1_C
        cov3 = COVERED_CARD2_P
        cov4 = COVERED_CARD2_C
        cov5 = WAR_PLAYED_P
        cov6 = WAR_PLAYED_C
    else:
        deck = computer
        cov1 = COVERED_CARD1_C
        cov2 = COVERED_CARD1_P
        cov3 = COVERED_CARD2_C
        cov4 = COVERED_CARD2_P
        cov5 = WAR_PLAYED_C
        cov6 = WAR_PLAYED_P
    screen.blit(pygame.transform.scale(deck.deck[-1].image, CARDSIZE),
                cov5)
    screen.blit(pygame.transform.scale(deck.deck[-2].image, CARDSIZE),
                cov6)
    screen.blit(pygame.transform.scale(deck.deck[-3].image, CARDSIZE),
                cov3)
    screen.blit(pygame.transform.scale(deck.deck[-4].image, CARDSIZE),
                cov4)
    screen.blit(pygame.transform.scale(deck.deck[-5].image, CARDSIZE),
                cov1)
    screen.blit(pygame.transform.scale(deck.deck[-6].image, CARDSIZE),
                cov2)


def render_screen(player, computer, plen, clen, screen):
    """update the screen"""
    global game_over, clear_text_p, clear_text_c
    player_count = CARD_FONT.render(
        "Player's Deck: {}".format(len(player)), True, BLACK,
        DARKGREEN)
    computer_count = CARD_FONT.render(
        "Computer's Deck: {}".format(len(computer)),
        True, BLACK, DARKGREEN)
    if plen == 0:
        clear_text_p = player_count.get_rect()
        clear_text_p.center = (130, 415)
        plen = 10
    if clen == 0:
        clear_text_c = computer_count.get_rect()
        clear_text_c.center = (500, 45)
        clen = 10
    pygame.draw.rect(screen, DARKGREEN, clear_text_p)
    pygame.draw.rect(screen, DARKGREEN, clear_text_c)

    player_rect = player_count.get_rect()
    player_rect.center = (130, 415)
    computer_rect = computer_count.get_rect()
    computer_rect.center = (500, 45)

    pygame.draw.rect(screen, DARKGREEN, computer_rect)
    screen.blit(player_count, player_rect)
    screen.blit(computer_count, computer_rect)
    if not player or not computer:
        game_over = True
    return plen, clen


def deal(screen):
    """deal cards to screen"""
    screen.blit(play_text, play_rect)
    screen.blit(CARDBACK, PLAY_DECK)
    screen.blit(CARDBACK, COMP_DECK)


def war(screen, ind):
    """play card game: War"""
    global CARD_FONT
    global reveal_rect
    global reveal_text
    global play_rect, play_text
    global pause
    global game_over

    pygame.init()
    CARD_FONT = pygame.font.Font('freesansbold.ttf', 25)
    game_deck = Deck(2, True)
    hands = game_deck.return_hands()
    player_deck = hands[0]
    computer_deck = hands[1]
    plen = 0
    clen = 0
    menu_rect, instr_rect = Main.menu_bar()
    reveal_text = CARD_FONT.render("Reveal Cards", True, WHITE, DARKGREEN)
    reveal_rect = reveal_text.get_rect()
    reveal_rect.center = (140, 50)
    play_text = CARD_FONT.render("Play", True, WHITE, DARKGREEN)
    play_rect = play_text.get_rect()
    play_rect.center = (500, 265)
    declared_war = False
    game_over = False
    pause = False
    deal(screen)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP and \
                    menu_rect.collidepoint(event.pos):
                Main.menu()
            elif event.type == MOUSEBUTTONUP and \
                    instr_rect.collidepoint(event.pos):
                instructions()
                reset_war_globals(screen)
                deal(screen)
                Main.menu_bar()
            if not game_over:
                if declared_war:
                    pygame.time.wait(2000)
                    pygame.draw.rect(screen, DARKGREEN, COVERED_CARD2_P)
                    pygame.draw.rect(screen, DARKGREEN, COVERED_CARD1_P)
                    pygame.draw.rect(screen, DARKGREEN, COVERED_CARD2_C)
                    pygame.draw.rect(screen, DARKGREEN, COVERED_CARD1_C)
                    pygame.draw.rect(screen, DARKGREEN, WAR_PLAYED_C)
                    pygame.draw.rect(screen, DARKGREEN, WAR_PLAYED_P)
                    pygame.draw.rect(screen, DARKGREEN, PLAYEDCARD_P)
                    pygame.draw.rect(screen, DARKGREEN, PLAYEDCARD_C)
                    pygame.draw.rect(screen, DARKGREEN, reveal_rect)
                    screen.blit(play_text, play_rect)
                    declared_war = False
                    pause = False
                declared_war, pause, player_deck, \
                    computer_deck = next_round(screen, event,
                                               declared_war, pause,
                                               player_deck,
                                               computer_deck)

                plen, clen = render_screen(player_deck, computer_deck,
                                           plen, clen, screen)
            else:
                has_won = end_game(computer_deck, screen)
                if event.type == KEYDOWN and event.key == K_y:
                    Main.resetglobals()
                    reset_war_globals(screen)
                    new_game(screen)
                elif event.type == KEYDOWN and event.key == K_n:
                    Main.menu()
                if not ind:
                    return has_won

        pygame.display.flip()


def next_round(screen, event, declared_war, stop,
               player_deck, computer_deck):
    """screen controls"""
    if event.type == MOUSEBUTTONUP:
        if play_rect.collidepoint(event.pos) and not stop:
            stop = play_war(player_deck, computer_deck, screen, stop)
        elif reveal_rect.collidepoint(event.pos):
            clear_screen(player_deck, computer_deck, screen)
            declared_war = True
            stop = False
    elif event.type == KEYDOWN:
        if event.key == K_RETURN and not stop:
            stop = play_war(player_deck, computer_deck, screen, stop)
        elif event.key == K_r or event.key == K_RETURN:
            clear_screen(player_deck, computer_deck, screen)
            declared_war = True
            stop = False
    return declared_war, stop, player_deck, computer_deck


def end_game(computer, screen):
    """end the game"""
    if computer:
        colors = RED
        win_text = CARD_FONT.render(
            "You played to the end, but lost.  Too bad", True, RED, BLACK)
        pygame.draw.rect(screen, DARKGREEN, PLAY_DECK + CARDSIZE)
        not_won = True
    else:
        colors = GREEN
        win_text = CARD_FONT.render("You played to the end, and won!.  "
                                    "Lucky!", True, GREEN, BLACK)
        pygame.draw.rect(screen, DARKGREEN, COMP_DECK + CARDSIZE)
        not_won = False
    win_rect = win_text.get_rect()
    win_rect.center = (330, 240)
    screen.blit(win_text, win_rect)
    win_text = CARD_FONT.render("Play Again? 'Y' or 'N'", True,
                                colors, BLACK)
    win_rect = win_text.get_rect()
    win_rect.center = (330, 290)
    screen.blit(win_text, win_rect)
    return not_won


def determine_card(deck, index):
    """in war, if deck is less than 3 cards, determine which card to use"""
    if len(deck) - 1 >= index + 2:
        return deck[index + 2]
    elif len(deck) - 1 >= index + 1:
        return deck[index + 1]
    else:
        try:
            return deck[index]
        except IndexError:
            return None


def declare_war(deck1, deck2, index, screen):
    """a single declaration of war; when players card == computers card"""
    global reveal_text, reveal_rect, play_rect, game_over, WIN
    deck1_playedcard = determine_card(deck1, index)
    deck2_playedcard = determine_card(deck2, index)
    if deck1_playedcard is None:
        game_over = True
        WIN = False
        return None
    elif deck2_playedcard is None:
        game_over = True
        WIN = True
        return None
    pygame.draw.rect(screen, DARKGREEN, play_rect)
    screen.blit(CARDBACK, COVERED_CARD1_P)
    screen.blit(CARDBACK, COVERED_CARD1_C)
    screen.blit(CARDBACK, COVERED_CARD2_P)
    screen.blit(CARDBACK, COVERED_CARD2_C)
    screen.blit(pygame.transform.scale(deck1_playedcard.image,
                                       CARDSIZE), WAR_PLAYED_P)
    screen.blit(pygame.transform.scale(deck2_playedcard.image,
                                       CARDSIZE), WAR_PLAYED_C)
    if deck1_playedcard > deck2_playedcard:
        if len(deck2) <= 3:
            game_over = True
        for a_card in range(index + 3):
            try:
                deck1.move_card()
                deck2.give_card(deck1)
                WIN = True
            except IndexError:
                pass
    elif deck1_playedcard < deck2_playedcard:
        if len(deck1) <= 3:
            game_over = True
        for a_card in range(index + 3):
            try:
                deck2.move_card()
                deck1.give_card(deck2)
                WIN = False
            except IndexError:
                pass
    else:
        declare_war(deck1, deck2, index + 3, screen)

    screen.blit(reveal_text, reveal_rect)


def instructions():
    """text for instructions box, and call function that adds it to
    the screen"""
    inst = ("Instructions:",  "1: Click 'PLAY' or press Enter to play"
            "a card", "2: If you have the higher value card, "
            "you win both cards",  "3: Aces are high", "__",
            "4: If the value of the cards are equal, war is declared",
            "5: Two cards are dealt face down, and a single car "
            "face up.  The player with the high valued face up card"
            "wins all eight cards.", "6: Click 'REVEAL CARDS' or "
            "press R to reveal cards and continue play", "__",  "__",
            "PRESS 'Q' TO RETURN TO GAME")
    Main.blit_instr(inst)


def new_game(screen, independent=True):
    """start a new game"""
    global CARDSIZE, CARDBACK, PLAY_DECK, COMP_DECK
    global PLAYEDCARD_C, PLAYEDCARD_P, COVERED_CARD1_P
    global COVERED_CARD1_C, COVERED_CARD2_P, COVERED_CARD2_C
    global WAR_PLAYED_P, WAR_PLAYED_C
    pygame.init()
    Main.resetglobals()
    reset_war_globals(screen)
    # pygame defaults
    CARDSIZE = (116, 162)
    CARDBACK = pygame.image.load('cards/cardback.png')
    PLAY_DECK = (50, 240)
    COMP_DECK = (460, 70)
    PLAYEDCARD_C = pygame.draw.rect(screen, DARKGREEN,
                                    (260, 70, 116, 162))
    PLAYEDCARD_P = pygame.draw.rect(screen, DARKGREEN,
                                    (260, 240, 116, 162))
    COVERED_CARD1_P = pygame.draw.rect(screen, DARKGREEN,
                                       (285, 240, 116, 162))
    COVERED_CARD1_C = pygame.draw.rect(screen, DARKGREEN,
                                       (240, 70, 116, 162))
    COVERED_CARD2_P = pygame.draw.rect(screen, DARKGREEN,
                                       (305, 240, 116, 162))
    COVERED_CARD2_C = pygame.draw.rect(screen, DARKGREEN,
                                       (220, 70, 116, 162))
    WAR_PLAYED_P = pygame.draw.rect(screen, DARKGREEN,
                                    (325, 240, 116, 162))
    WAR_PLAYED_C = pygame.draw.rect(screen, DARKGREEN,
                                    (200, 70, 116, 162))
    pygame.display.flip()

    # play war!
    has_won = war(screen, independent)
    return has_won
