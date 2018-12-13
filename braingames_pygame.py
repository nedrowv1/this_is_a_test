import random
import sys
from collections import Counter
import Grandmas_Game_Closet as Main
import pygame
from pygame.locals import *
import shelve

# Colors used

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
TEAL = (15, 225, 210)

# classes


class Peg(object):
    """a single peg
    attributes: color, location"""
    def __init__(self, peg_color, loc_index=None):
        """given a color and a location, create a peg
        location is a pygame location, not an index value"""
        self.color = peg_color
        self.location = loc_index

    def __eq__(self, other):
        """compare two pegs together.  if other is not a peg,
        then assume inequality"""
        if isinstance(other, Peg):
            return self.color == other.color
        else:
            return False

    def hue(self):
        """return the color of the peg"""
        return self.color


class PegRow(object):
    """a row of pegs, either the answer or a player guess

    attributes: pegs (the set of pegs in the row),
    pegchoices (the available colors for a given peg"""
    def __init__(self, numpegs=5):
        """create a row of pegs the size of the row (default is 5"""
        self.pegs = [None] * numpegs

        self.pegchoices = {"red": RED, "blue": BLUE, "green": GREEN,
                           "purple": PURPLE, "yellow": YELLOW,
                           "tan": TAN, "white": WHITE, "black": BLACK,
                           "orange": ORANGE}

    def __getitem__(self, c_index):
        """returned the peg located at a given index"""
        return self.pegs[c_index]


class AnswerRow(PegRow):
    """the Answer version of a pegrow.  Creates a randome selection
    of pegs based of the available colors.  no additional attributes"""
    def __init__(self, numpegs=5):
        pegcolors = ("red", "blue", "green", "purple", "yellow", "tan",
                     "white", "black", "orange")
        super(AnswerRow, self).__init__()
        for p_index in range(len(self.pegs)):
            blind_peg = random.choice(pegcolors)
            self.pegs[p_index] = (Peg(self.pegchoices[blind_peg], None))


class GuessRow(PegRow):
    """the Guess version of a pegrow.  has additional methods for
    manipulation.  Can be used to create a two player version of
    the game.  no additional attributes"""
    def __init__(self, numpegs=5):
        """import initilizations from PegRow"""
        super(GuessRow, self).__init__()
        self.answer_key = [WHITE] * len(self.pegs)

    def add_peg(self, colors, p_index, loc_index):
        """adds a peg to the guess row"""
        self.pegs[p_index] = Peg(colors, loc_index)

    def is_equal(self, other):
        """checks how many of a given color from a given PegRow
        are in the GuessRow.  returns a list of colors, not a
        boolean so did not use __eq__"""
        self.answer_key = [WHITE] * len(other.pegs)
        cntr = 0
        a_counter = {RED: 0, BLUE: 0, GREEN: 0, YELLOW: 0, PURPLE: 0,
                     ORANGE: 0, TAN: 0, WHITE: 0, BLACK: 0}
        others = []
        for pIndex in range(len(other.pegs)):
            others.append(other.pegs[pIndex].hue())
        b_counter = Counter(others)
        """populate for 1 to len(pegs) the number of correct colors"""
        for pIndex in range(len(self.pegs)):
            if type(self.pegs[pIndex]) != int:  # catch init errors
                if self.pegs[pIndex] in other.pegs:
                    if a_counter[self.pegs[pIndex].hue()] < \
                            b_counter[self.pegs[pIndex].hue()]:
                        self.answer_key[cntr] = RED
                        a_counter[self.pegs[pIndex].hue()] += 1
                        cntr += 1
        cntr = 0
        # overwrite correct colors (above) with correct color and location
        for peg in range(5):
            if self.pegs[peg] == other.pegs[peg]:
                self.answer_key[cntr] = GREEN
                cntr += 1
        return self.answer_key

    def tup(self):
        """used to save self.pegs as immutable form to the list of
        answers given"""
        return tuple(self.pegs)


# pygame helper functions
def submit(screen):
    """check if the submitted answer is the
    hidden answer, clear the screen of the guess"""
    correct_pegs = TEMP_PEGS.is_equal(HIDDEN_COLORS)
    greens = 0
    for p in correct_pegs:
        if p == GREEN:
            greens += 1
    if greens == 5:  # five greens equalivant to TEMP_PEGS == HIDDEN_COLORS
        win_text = pygame.font.Font('freesansbold.ttf', 25)
        win_render = win_text.render("YOU WIN!", True, WHITE, BLACK)
        win_rect = win_render.get_rect()
        win_rect.center = (340, 354)
        screen.blit(win_render, win_rect)
        return None, None   # end game

    else:
        ANSWER_TREE.insert(0, (
            correct_pegs, TEMP_PEGS.tup()))
        if len(ANSWER_TREE) > 8:
            max_show = 8  # the screen only has space for 8 answers
        else:
            max_show = len(ANSWER_TREE)
        print_guesses(screen, last_guess=max_show)
        # hide previous guess
        pygame.draw.rect(screen, NAVY, pygame.Rect(350, 125, 300, 100))
        peg_hole(screen, GUESS_PEG1, GREY)
        peg_hole(screen, GUESS_PEG2, GREY)
        peg_hole(screen, GUESS_PEG3, GREY)
        peg_hole(screen, GUESS_PEG4, GREY)
        peg_hole(screen, GUESS_PEG5, GREY)
    return 0, max_show


def print_guesses(screen, first_guess=0, last_guess=1, answer_tree_x=44,
                  answer_tree_y=115):
    """print a given set of 8 or fewer answers to the screen"""
    for print_index in range(len(ANSWER_TREE)):
        if first_guess <= print_index <= last_guess:
            for a_color in range(5):
                loc = (answer_tree_x, answer_tree_y)
                peg = ANSWER_TREE[print_index][1]
                try:
                    pygame.draw.circle(screen, peg[a_color].hue(),
                                       loc, GUESS_RADIUS)
                except AttributeError:  # for accidental submissions
                    warning_box("Please select all five colors", screen)
                    answer_tree_x -= 50 * a_color
                    for bad_color in range(a_color+1):
                        pygame.draw.circle(screen, GREY,
                                           (answer_tree_x, answer_tree_y),
                                           GUESS_RADIUS)
                        answer_tree_x += 50
                    return None
                answer_tree_x += 50
            pegs = ANSWER_TREE[print_index][0]
            for answer in pegs:  # print is_equal
                test_text = pygame.font.Font('freesansbold.ttf', 25)
                test_button = test_text.render("|", True, answer, GREY)
                test_rect = test_button.get_rect()
                test_rect.center = (answer_tree_x, answer_tree_y)
                screen.blit(test_button, test_rect)
                answer_tree_x += 5
            answer_tree_y += 40
            answer_tree_x = 44


def warning_box(text, screen):
    """print given text to the warning box at the top of the screen"""
    text_list = []
    temp_text = ""
    next_line = 50
    warn_location = (375, 25, 220, 125)
    text_center = 485
    while len(text) > 0:
        temp_text += text[0]
        try:
            text = text[1:]
            # limit length of line to 10 characters
            if len(temp_text) >= 10 and temp_text[-1] == " ":
                text_list.append(temp_text)
                temp_text = ""
        except IndexError:
            pass
    temp_text += text
    text_list.append(temp_text)
    warning_text = [""] * len(text_list)
    warning_frame = [""] * len(text_list)
    warning_rect = [""] * len(text_list)
    pygame.draw.rect(screen, GREY, pygame.Rect(warn_location))
    for line in range(len(text_list)):
        warning_text[line] = pygame.font.Font('freesansbold.ttf', 20)
        warning_frame[line] = warning_text[line].render(text_list[line],
                                                        True, RED, GREY)
        warning_rect[line] = warning_frame[line].get_rect()
        warning_rect[line].center = (text_center, next_line)
        screen.blit(warning_frame[line], warning_rect[line])
        next_line += 20


def is_color(pos, col_index, attempt, screen):
    """add peg to guess, and verify no more than 5 pegs are added"""
    attempt_x, attempt_y = attempt
    total_colors = 5
    nocollide_flag = False
    warn_txt = "To exchange a peg, click on the " \
               "peg you wish to edit first."
    loc_color_switcher = {0: RED, 1: GREEN, 2: BLUE, 3: YELLOW, 4: PURPLE,
                          5: TAN, 6: ORANGE, 7: WHITE, 8: BLACK}
    x_corr_switcher = {0: TEMP_X_1, 1: TEMP_X_2, 2: TEMP_X_3, 3: TEMP_X_4,
                       4: TEMP_X_5}
    for i in range(9):
        if CIRCLE[i].collidepoint(pos):
            if col_index < total_colors:
                return loc_color_switcher[i], \
                       col_index, (attempt_x, attempt_y)
            else:
                warning_box(warn_txt, screen)
        nocollide_flag = True
    if nocollide_flag:
        try:
            for i in range(5):
                if TEMP_PEGS.pegs[i].location.collidepoint(pos):
                    return DARKGREY, i, (x_corr_switcher[i], attempt_y)
        except IndexError:
            pass
        except AttributeError:
            pass
    return None, col_index, attempt


def draw_shield(size, screen):
    """hide answer"""
    left = 15
    top = 15
    length = 320
    pygame.draw.rect(screen, GREY, SHIELD)
    peg_hole(screen, SOLVED_PEG1)
    peg_hole(screen, SOLVED_PEG2)
    peg_hole(screen, SOLVED_PEG3)
    peg_hole(screen, SOLVED_PEG4)
    peg_hole(screen, SOLVED_PEG5)
    if size > 0:
        pygame.draw.rect(screen, WHITE, (left, top, length, size))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def peg_hole(screen, location, outercolor=DARKGREY, innercolor=BLACK,
             big_radius=10, small_radius=5):
    """Draw pegs"""
    pygame.draw.circle(screen, outercolor, location, big_radius, 0)
    pygame.draw.circle(screen, innercolor, location, small_radius, 0)


def get_pegs(screen, prevcolor, colors=20):
    """used in windows and linux machines to animate shield closing"""
    if colors > 0:
        pygame.draw.rect(screen, prevcolor, SHIELD)
        randcolor = random.choice(PEGS)
        pygame.time.wait(100)
        pygame.display.update()
        get_pegs(screen, randcolor, colors - 1)
    else:
        pygame.draw.rect(screen, WHITE, SHIELD)
        pygame.display.update()


def end_game(chk1, chk2):
    """check if game won; chk1 and chk2 come from submit function"""
    if chk1 is None and chk2 is None:
        return False
    return True


def blit_win(screen):
    """finish game"""
    pygame.draw.rect(screen, GREY, SHIELD)
    peg_hole(screen, SOLVED_PEG1, outercolor=HIDDEN_COLORS[0].hue(),
             big_radius=GUESS_RADIUS, small_radius=0)
    peg_hole(screen, SOLVED_PEG2, outercolor=HIDDEN_COLORS[1].hue(),
             innercolor=HIDDEN_COLORS[1].hue(), big_radius=GUESS_RADIUS,
             small_radius=0)
    peg_hole(screen, SOLVED_PEG3, outercolor=HIDDEN_COLORS[2].hue(),
             innercolor=HIDDEN_COLORS[2].hue(), big_radius=GUESS_RADIUS,
             small_radius=0)
    peg_hole(screen, SOLVED_PEG4, outercolor=HIDDEN_COLORS[3].hue(),
             innercolor=HIDDEN_COLORS[3].hue(), big_radius=GUESS_RADIUS,
             small_radius=0)
    peg_hole(screen, SOLVED_PEG5, outercolor=HIDDEN_COLORS[4].hue(),
             innercolor=HIDDEN_COLORS[4].hue(), big_radius=GUESS_RADIUS,
             small_radius=0)
    warning_box("Congratulations!  You WON!\n New Game? Press 'Y' or 'N'",
                screen)
    for event in pygame.event.get():
        if event.type == KEYUP and event.key == K_y:
            new_game(screen)
        elif event.type == KEYUP and event.key == K_n:
            Main.menu()
        elif event.type == QUIT or (event.type == KEYUP and (
                                    event.key == K_q or
                                    event.key == K_ESCAPE)):
            saved_game = shelve.open("SavedGame")
            saved_game['Story_Mode_Finished'] = 1
            # save location story mode
            saved_game.close()
            pygame.quit()
            sys.exit()

    pygame.display.update()


def new_game(screen, independant=True):
    """Start a new game"""
    global CIRCLE, SHOW_LAST, ANSWER_TREE
    global HIDDEN_COLORS, TEMP_PEGS
    pygame.init()
    Main.resetglobals()
    reset_master_globals()
    pygame.display.set_caption('Brain Games')
    HIDDEN_COLORS = AnswerRow()
    CIRCLE = []
    draw_screen(screen)
    for coverage in range(0, SHIELD_HEIGHT, 4):
        draw_shield(coverage, screen)
    ANSWER_TREE = []
    TEMP_PEGS = GuessRow()
    SHOW_LAST = len(ANSWER_TREE)

    peg_color = WHITE
    get_pegs(screen, peg_color)
    play = True
    first = last = 0
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and \
               menu_rect.collidepoint(event.pos):
                Main.menu()
            elif event.type == MOUSEBUTTONUP and \
                    instr_rect.collidepoint(event.pos):
                    instructions()
                    draw_screen(screen)
                    if len(ANSWER_TREE) > 8:
                        max_show = 8
                    else:
                        max_show = len(ANSWER_TREE)
                    print_guesses(screen=screen, last_guess=max_show)
            if play:
                play, first, last, peg_color = \
                    update_board(screen, event, first,
                                 last, peg_color, play)
            else:
                if independant:
                    reset_game(screen, event)
                else:
                    return False
        pygame.display.update()


def reset_game(screen, event):
    """clear board for new game"""
    blit_win(screen)
    if event.type == QUIT:
        saved_game = shelve.open("SavedGame")
        saved_game['Story_Mode_Finished'] = 1
        # save location story mode
        saved_game.close()
        pygame.quit()
        sys.exit()
    if event.type == KEYUP and event.key == K_y:
        reset_master_globals()
        Main.resetglobals()
        new_game(screen)
    elif event.type == KEYUP and event.key == K_n:
        Main.menu()

            
def update_board(screen, event, first, last, peg_color, flag):
    """update the board as guesses are made"""
    global LOCATION, POSITION, GUESS_LIST_SCREEN
    
    pygame.draw.rect(screen, WHITE, SHIELD)
    if event.type == QUIT:
        saved_game = shelve.open("SavedGame")
        saved_game['Story_Mode_Finished'] = 1
        # save location story mode
        saved_game.close()
        pygame.quit()
        sys.exit()
    elif event.type == MOUSEBUTTONUP \
            and SUBMIT_BUTTON.collidepoint(event.pos):
        first, last = submit(screen)
        LOCATION = 0
        POSITION = GUESS_PEG1
        flag = end_game(first, last)
    elif event.type == MOUSEBUTTONUP and \
            ARROW_UP_BOX.collidepoint(event.pos) and \
            len(ANSWER_TREE) > 8:
        if first <= len(ANSWER_TREE) - 8:
            GUESS_LIST_SCREEN = pygame.draw.rect(screen, GREY,
                                                 (15, 15,
                                                  320, 440))
            print_guesses(screen, first + 1, last + 1)
            first += 1
            last += 1
    elif event.type == MOUSEBUTTONUP and \
            ARROW_DOWN_BOX.collidepoint(event.pos) and \
            len(ANSWER_TREE) > 8:
        if last >= 9:
            GUESS_LIST_SCREEN = pygame.draw.rect(screen,
                                                 GREY,
                                                 (15, 15,
                                                  320, 440))
            print_guesses(screen, first - 1, last - 1)
            first -= 1
            last -= 1
    elif event.type == MOUSEBUTTONUP:
        peg_color, LOCATION, POSITION = is_color(event.pos,
                                                 LOCATION,
                                                 POSITION,
                                                 screen)
        if peg_color is not None and peg_color != DARKGREY:
            TEMP_PEGS.add_peg(peg_color, LOCATION,
                              pygame.draw.circle(screen,
                                                 peg_color,
                                                 POSITION,
                                                 PEG_RADIUS))
            LOCATION += 1
            x, y = POSITION
            x += 55
            POSITION = (x, y)
            pygame.draw.rect(screen, NAVY,
                             pygame.Rect(375, 25, 250, 125))
            # if error message, hide box
        elif peg_color == DARKGREY:
            # replace pegs
            pygame.draw.circle(screen, NAVY, POSITION,
                               PEG_RADIUS)
            TEMP_PEGS.add_peg(loc_index=peg_hole(screen,
                                                 POSITION,
                                                 GREY),
                              colors=GREY,
                              p_index=LOCATION)
    return flag, first, last, peg_color
            
            
def draw_screen(screen):
    """Create the game board"""
    global GUESS_LIST_SCREEN
    global SUBMIT_BUTTON, ARROW_UP_BOX, ARROW_DOWN_BOX
    global COLLECTION_PEGS_X, COLLECTION_PEGS_Y
    global menu_rect, instr_rect
    # import menu_rect and instr_rect as global

    reset_master_globals()
    screen.fill(BGCOLOR)
    menu_rect, instr_rect = Main.menu_bar()

    submit_text = pygame.font.Font('freesansbold.ttf', 25)
    submit_button = submit_text.render('Submit', True, DARKGREEN, WHITE)
    submit_rect = submit_button.get_rect()
    submit_rect.center = (500, 245)

    GUESS_LIST_SCREEN = pygame.draw.rect(screen, GREY, (15, 15, 320, 440))
    SUBMIT_BUTTON = pygame.draw.rect(screen, WHITE, (451, 225, 100, 40))

    arrow_up = pygame.image.load('scrollarrow.png')
    arrow_down = pygame.transform.flip(arrow_up, False, True)

    peg_hole(screen, SOLVED_PEG1)
    peg_hole(screen, SOLVED_PEG2)
    peg_hole(screen, SOLVED_PEG2)
    peg_hole(screen, SOLVED_PEG4)
    peg_hole(screen, SOLVED_PEG5)

    peg_hole(screen, GUESS_PEG1, GREY)
    peg_hole(screen, GUESS_PEG2, GREY)
    peg_hole(screen, GUESS_PEG3, GREY)
    peg_hole(screen, GUESS_PEG4, GREY)
    peg_hole(screen, GUESS_PEG5, GREY)
    screen.blit(submit_button, submit_rect)
    ARROW_UP_BOX = Rect(351, 225, 40, 40)
    screen.blit(arrow_up, (351, 225))
    screen.blit(arrow_down, (351, 270))
    ARROW_DOWN_BOX = Rect(351, 270, 40, 40)

    for peg in PEGS:
        CIRCLE.append(pygame.draw.circle(screen, peg,
                                         (COLLECTION_PEGS_X,
                                          COLLECTION_PEGS_Y), PEG_RADIUS))
        if peg != PURPLE:
            COLLECTION_PEGS_X += 55
        else:
            COLLECTION_PEGS_Y -= 55
            COLLECTION_PEGS_X = 400


def reset_master_globals():
    """reset all widely used variables to new game status"""
    global SHIELD, FPS
    global PEG_RADIUS, BGCOLOR, FPSCLOCK
    global SOLVED_PEG1, SOLVED_PEG2, SOLVED_PEG3, SOLVED_PEG4, SOLVED_PEG5
    global GUESS_PEG1, GUESS_PEG2, GUESS_PEG3, GUESS_PEG4, GUESS_PEG5
    global COLLECTION_PEGS_X, COLLECTION_PEGS_Y, PEGS
    global BLOCKER, CIRCLE, TEMP_PEGS, LOCATION, POSITION, ANSWER_TREE
    global TEMP_X_1, TEMP_X_2, TEMP_X_3, TEMP_X_4, TEMP_X_5
    global GUESS_RADIUS, SHIELD_HEIGHT, SHOW_LAST
    FPS = 30
    FPSCLOCK = pygame.time.Clock()
    SHIELD = (15, 15, 320, 64)
    PEG_RADIUS = 20
    BGCOLOR = NAVY
    SOLVED_PEG1 = (44, 44)
    SOLVED_PEG2 = (110, 44)
    SOLVED_PEG3 = (176, 44)
    SOLVED_PEG4 = (242, 44)
    SOLVED_PEG5 = (308, 44)
    GUESS_PEG1 = (375, 175)
    GUESS_PEG2 = (430, 175)
    GUESS_PEG3 = (480, 175)
    GUESS_PEG4 = (540, 175)
    GUESS_PEG5 = (595, 175)
    COLLECTION_PEGS_X = 375
    COLLECTION_PEGS_Y = 407
    PEGS = (RED, GREEN, BLUE, YELLOW, PURPLE, TAN, ORANGE, WHITE, BLACK)
    BLOCKER = pygame.Rect(SHIELD)
    LOCATION = 0
    POSITION = GUESS_PEG1
    TEMP_X_1 = 375
    TEMP_X_2 = 430
    TEMP_X_3 = 485
    TEMP_X_4 = 540
    TEMP_X_5 = 595
    GUESS_RADIUS = 15
    SHIELD_HEIGHT = 65


def instructions():
    """instructions for play, call functin to print to screen"""
    inst = ("Instructions:",  "1: Click a colored circle "
            "to choose a peg.", "2: When all five colors",
            "are chosen, press submit",
            "3: The number of colors will appear beside your"
            " choices", "4: The number in the correct "
            "location will appear in green, the number of "
            "the correct color in the wrong spot will appear "
            "in red.", "5: Guess the hidden pattern", "__",
            "__", "PRESS 'Q' TO RETURN TO GAME")
    Main.blit_instr(inst)

