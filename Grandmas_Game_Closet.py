import pygame
from pygame.locals import *
import braingames_pygame as brain_games
import hangman_pygame as hangman
import war_pygame as war
import typewriter as tw
import yacht_pygame as yacht
import shelve


# colors
CREAM = (255, 222, 163)
ROYAL = (80, 45, 114)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TEAL = (15, 225, 210)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREEN = (20, 100, 20)
GREY = (100, 100, 100)
NAVY = (60, 60, 100)


def draw_shield(size, screen):
    """hide answer"""
    left = 0
    top = 0
    length = 640
    if size > 0:
        pygame.draw.rect(screen, CREAM, (left, top, length, size))
    pygame.display.update()
    clock.tick(60)


def blit_instr(instructions):
    """print instruction block to the screen"""
    inst = True
    next_line = 70
    instr_location = (80, 50, 500, 400)
    pygame.draw.rect(SCREEN, BLACK, instr_location)
    for text in instructions:
        text_list = []
        temp_text = ""
        while len(text) > 0:
            temp_text += text[0]
            try:
                text = text[1:]
                if len(temp_text) >= 45 and temp_text[-1] == " ":
                    text_list.append(temp_text)
                    temp_text = ""
            except IndexError:
                pass
        temp_text += text
        text_list.append(temp_text)
        instr_frame = [""] * len(text_list)
        instr_rect = [""] * len(text_list)
        instr_text = pygame.font.Font('freesansbold.ttf', 20)

        for line in range(len(text_list)):

            instr_frame[line] = instr_text.render(
                                text_list[line], True, WHITE, BLACK)
            instr_rect[line] = instr_frame[line].get_rect()
            instr_rect[line].left = 90
            instr_rect[line].top = next_line
            SCREEN.blit(instr_frame[line], instr_rect[line])
            next_line += 21
    while inst:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                inst = False
            elif event.type == KEYUP and event.key == K_q:
                inst = False
        pygame.display.update()
    return None


def resetglobals():
    """reset pygame global variables for each new game"""
    global WINWIDTH, WINHEIGHT, SCREEN
    WINWIDTH = 640
    WINHEIGHT = 500
    SCREEN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    return SCREEN


def menu_items(text, a_font, y_cor, cntr):
    """draw main menu"""
    circle = pygame.draw.circle(SCREEN, RED, (95, cntr), 15)
    text = a_font.render(text, True, ROYAL, CREAM)
    rect = text.get_rect()
    rect.left = 120
    rect.top = y_cor
    return circle, text, rect


def writestuff(text, bgcolor, text_color):
    """write to the screen

    typewriter.py based on code found online, modified to take
    parameters.  I have no idea how it works, but it looks really
    cool"""
    all_sprites = pygame.sprite.Group()
    board = tw.Board(WINWIDTH, WINHEIGHT, bgcolor)
    cursor = tw.Cursor(board, text_color)
    all_sprites.add(cursor, board)
    cursor.write(text)

    running = True
    while running:
        all_sprites.update()
        SCREEN.fill(bgcolor)
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                running = False
            elif event.type == QUIT:
                saved_game = shelve.open("SavedGame")
                saved_game['Story_Mode_Finished'] = saved
                # save location story mode
                saved_game.close()
                pygame.quit()


def story_mode():
    """the first time playing the game, play through story mode, having
    to win each game before continuing on to the next one."""
    global SCREEN, word, definition
    global clock, saved
    clock = pygame.time.Clock()
    pygame.display.set_caption("Grandma's Game Closet")
    SCREEN.fill(BLACK)
    # save = 4; game has started
    if saved == 4:
        text = """...
You step down into a darkened hallway.

The air smells of cookies and Noxima.

Distantly a cat meows...

You flip a switch, the lights come on ...

..."""
        writestuff(text, BLACK, GREEN)
        text = """The door stands before you...

...

...

...You open it..."""
        writestuff(text, WHITE, BLACK)
    # start war
        text = """A stack of boxes teeters precariously...

You reach up to protect your face...

but all that falls is a deck of cards.

Before you can react, the air shifts...

...the game begins!"""

        writestuff(text, DARKGREEN, BLACK)

        while True:
            not_won = war.new_game(SCREEN, False)
            if not not_won:
                saved = 3
                break
            else:
                text = """Laughter drifts around you and the cards shuffle.
    
    You have no choice but to play again..."""
                writestuff(text, DARKGREEN, BLACK)
    # saved = 3; beat war; jump to yacht
    if saved == 3:
        text = """The cards settle to the ground, the game over.

You've won.  Before you can take a breath,
another box begins to fall...

You jump out of the way of the flying pencil.

There's something written on the piece of paper
that falls from the lid..."""

        writestuff(text, GREY, RED)
        text = """Win at 200, it says, scribbled in curly script.
    
Win at 200?  What could that mean?
    
And then the dice begin to roll..."""
        writestuff(text, GREY, RED)
        while True:
            not_won = yacht.new_game(SCREEN, False)
            if not not_won:
                saved = 2
                break
            else:
                text = """Laughter drifts around you...
    
    ...the dice jump back into the cup.
    
    You have no choice but to play again..."""
                writestuff(text, GREY, RED)
    # saved = 2; beat yacht, go right to hangman
    if saved == 2:
        text = """The dice fall silent, the game over.

You've won.  Pushing the dice and papers away,
you see another box tumbling down.

You catch this one, a shoebox.

The notebook falls out...

The pen with it..."""
        writestuff(text, ROYAL, CREAM)
        while True:
            not_won, word, definition = hangman.new_game(SCREEN, False)
            if not not_won:
                saved = 1
                break
            else:
                text = """The laughter fills your ears.
    
    You'd swear the little line drawing of a man
    on a gallows swings in an unfelt breeze.
    
    You have no choice but to play again..."""

                writestuff(text, ROYAL, CREAM)
    # saved = 1; beat hangman, go right to braingames
    if saved == 1:
        text = """The pen settles,
the word, {},
scribbled on the page.

It means {}.

It's over.  It has to be over.

But no...another box,

all plastic and rough edges, tumbles down...

...into your outstretched hands...""".format(word, definition)
        writestuff(text, NAVY, WHITE)
        while True:
            not_won = brain_games.new_game(SCREEN, False)
            if not not_won:
                break
        text = """The lights flicker, then steady.
    
    Around you is the detritus of games played.
    
    Outside, a storm settles...
    
    ...from raging to light drizzle.
    
    A woman's voice calls your name.
    
    You look up...
    
    Of course...
    
    This was just..."""

        writestuff(text, WHITE, BLACK)
    text = """Grandma's Game Closet"""
    writestuff(text, BLACK, TEAL)
    for i in range(0, WINHEIGHT, 4):
        draw_shield(i, SCREEN)
    # saved = 0, bypass story mode
    saved = 0
    menu()


def menu():
    """if story mode is beaten, go to menu"""
    SCREEN.fill(CREAM)
    font = pygame.font.Font('freesansbold.ttf', 40)
    menu_text = font.render("GRANDMA'S GAME CLOSET", True, ROYAL,
                            CREAM)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (320, 20)
    SCREEN.blit(menu_text, menu_rect)
    font = pygame.font.Font('freesansbold.ttf', 30)
    
    master_circle, master_text, master_rect = menu_items("Play Brain "
                                                         "Games", font,
                                                         93, 105)
    SCREEN.blit(master_text, master_rect)

    hangman_circle, hangman_text, hangman_rect = menu_items("Play Hangman",
                                                            font, 128, 140)
    SCREEN.blit(hangman_text, hangman_rect)

    war_circle, war_text, war_rect = menu_items("Play War", font,
                                                163, 175)
    SCREEN.blit(war_text, war_rect)

    yacht_circle, yacht_text, yacht_rect = menu_items("Play Yacht", font,
                                                      198, 210)
    SCREEN.blit(yacht_text, yacht_rect)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                saved_game = shelve.open("SavedGame")
                saved_game['Story_Mode_Finished'] = saved
                saved_game.close()
                pygame.quit()
            elif event.type == MOUSEBUTTONUP:
                if master_rect.collidepoint(event.pos) or \
                   master_circle.collidepoint(event.pos):
                        brain_games.new_game(SCREEN)
                elif hangman_rect.collidepoint(event.pos) or \
                        hangman_circle.collidepoint(event.pos):
                    hangman.new_game(SCREEN)
                elif war_rect.collidepoint(event.pos) or \
                        war_circle.collidepoint(event.pos):
                    war.new_game(SCREEN)
                elif yacht_rect.collidepoint(event.pos) or \
                        yacht_circle.collidepoint(event.pos):
                    yacht.new_game(SCREEN)
            elif event.type == MOUSEBUTTONDOWN:
                if master_rect.collidepoint(event.pos) or \
                   master_circle.collidepoint(event.pos):
                    master_circle = pygame.draw.circle(SCREEN, GREEN,
                                                       (95, 105), 15)
                elif hangman_rect.collidepoint(event.pos) or \
                        hangman_circle.collidepoint(event.pos):
                    hangman_circle = pygame.draw.circle(SCREEN, GREEN,
                                                        (95, 140), 15)
                elif war_rect.collidepoint(event.pos) or \
                        war_circle.collidepoint(event.pos):
                    war_circle = pygame.draw.circle(SCREEN, GREEN,
                                                    (95, 175), 15)
                elif yacht_rect.collidepoint(event.pos) or \
                        yacht_circle.collidepoint(event.pos):
                    yacht_circle = pygame.draw.circle(SCREEN, GREEN,
                                                      (95, 210), 15)
        pygame.display.update()


def menu_bar():
    """each mini-game has a menu bar that allows direct access to
    the main menu.  This allows story mode to be bypassed after
    starting war, but the game state will not be saved"""
    pygame.draw.rect(SCREEN, TEAL, (0, 460, 640, 40))
    menu_font = pygame.font.Font('freesansbold.ttf', 15)
    menu_txt = menu_font.render("Menu", True, BLACK, TEAL)
    menu_rect = menu_txt.get_rect()
    menu_rect.center = (60, 480)
    SCREEN.blit(menu_txt, menu_rect)
    instr_txt = menu_font.render("Instructions", True, BLACK, TEAL)
    instr_rect = instr_txt.get_rect()
    instr_rect.center = (150, 480)
    SCREEN.blit(instr_txt, instr_rect)
    return menu_rect, instr_rect


if __name__ == "__main__":
    global saved
    shelfFile = shelve.open("SavedGame")
    try:
        saved = shelfFile['Story_Mode_Finished']
        if saved == 1:
            global word, definition
            word = "saved"
            definition = "Keep and store up something for future use."
        # save story mode location
    except KeyError:
        # if first game, play through entire story mode
        saved = 4
    shelfFile.close()
    pygame.init()
    resetglobals()
    if saved == 0:
        menu()
    else:
        story_mode()

