import random
from collections import Counter
import Grandmas_Game_Closet as Main
import pygame
from pygame.locals import *
import shelve

# colors
GREY = (225, 225, 225)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Die(object):
    """a single die, top face
        faces: the number of sides on the die
        top: the value of the top side face
        attributes: faces, top"""

    def __init__(self, faces):
        """standard die has a set number of faces and a value for the face
        that is pointing upward"""
        self.faces = faces
        self.top = self.roll()

    def __eq__(self, other):
        """check if two die, or a number representing the upward face
        match"""
        if isinstance(other, Die):
            return self.top == other.top
        return self.top == other

    def __add__(self, other):
        """add a number to a die, or two die together"""
        if isinstance(other, Die):
            return self.top + other.top
        return self.top + int(other)

    def __radd__(self, other):
        """add a number to a die"""
        return self.top + int(other)

    def roll(self):
        """reroll die"""
        self.top = random.randint(1, self.faces)
        return self.top

    def __hash__(self):
        """allow a die to be used as the key in a dictionary, I guess?
        not sure why I had to add it, but the ditionaries didn't work
        without it"""
        return hash(str(self))

    def __lt__(self, other):
        """compare die"""
        if isinstance(other, Die):
            return self.top < other.top
        else:
            return self.top < other

    def __gt__(self, other):
        """compare die"""
        if isinstance(other, Die):
            return self.top > other.top
        return self.top > other


class YachtDie(Die):
    """a die specifically for use in Yacht.  had additional attribute
    to check if the dice should be rolled or not, and one for pygame
    integration

    attributes: held_color(for pygame), hold"""
    def __init__(self):
        """held_color is for pygae integration, hold=True prevents the die
        from rolling in a given round"""
        super(YachtDie, self).__init__(6)
        self.held_color = None
        self.hold = False

    def is_held(self):
        """return the value of hold"""
        return self.hold


class YatzeeRoll(object):
    """1 - 5 dice rolled together
    attributes: dice, size, rolls_left"""

    def __init__(self, size=5, maxrolls=3):
        """standard Yacht game uses five die, and three rolls."""
        self.size = size
        self.dice = []
        self.rolls_left = maxrolls
        for i in range(size):
            self.dice.append(YachtDie())
            self.dice[i].held_color = WHITE

    def is_held(self, index):
        """checks if a die of a given index is held"""
        return self.dice[index].is_held()

    def die(self, index):
        """return a die of a specific index"""
        return self.dice[index]

    def roll(self):
        """roll die in hand"""
        if self.rolls_left > 0:
            for i in range(self.size):
                if not self.is_held(i):
                    self.die(i).roll()
            self.rolls_left -= 1
        else:
            raise Exception("reached maximum number of rolls")

    def hold(self, index):
        """hold a die"""
        self.dice[index].hold = True
        self.dice[index].held_color = RED

    def release_hold(self, index):
        """release hold on a die"""
        self.dice[index].hold = False
        self.dice[index].held_color = WHITE

    def end_turn(self):
        """start the next round of play by resetting the number of
        rolls available and removing the hold from all die"""
        self.rolls_left = 3
        for i in range(self.size):
            self.dice[i].hold = False
            self.dice[i].held_color = WHITE

    def tops(self):
        """used for 'in' operation and for 'Counter' object
        essentially converting the Die into an integer"""
        for i in self.dice:
            yield i.top

    def __contains__(self, value):
        """checks if a value is in a roll"""
        return value in self.tops()

    def __getitem__(self, index):
        """allows indexing"""
        return self.dice[index]

    def __iter__(self):
        """iterate through dice in hand"""
        self.i = 0
        return self

    def __next__(self):
        """iternate through dice in hand"""
        if self.i < self.size:
            result = self.dice[self.i]
            self.i += 1
            return result
        else:
            raise StopIteration

    def sort(self):
        """sort dice in hand"""
        self.dice.sort()
        return self


def reset_yacht_globals():
    """reset yacht specific global variables"""
    global lastupper, lastlower, FONT20, FONT16, FONT50, FONT18
    global upper_scores, lower_scores, upscores, lowscores

    FONT20 = pygame.font.Font('freesansbold.ttf', 20)
    FONT16 = pygame.font.Font('freesansbold.ttf', 16)
    FONT50 = pygame.font.Font('freesansbold.ttf', 50)
    FONT18 = pygame.font.Font('freesansbold.ttf', 18)
    lastupper = {"Ones": 0, "Twos": 0, "Threes": 0, "Fours": 0, "Fives": 0,
                 "Sixes": 0, "Bonus": 0, "Total": 0}
    lastlower = {"Three of a Kind": 0, "Four of a Kind": 0,
                 "Small Straight": 0, "Large Straight": 0,
                 "Full House": 0, "Chance": 0, "Yacht": 0,
                 "Yacht Bonus": 0, "Total": 0, "Final Score": 0}
    upper_scores = {"Ones": 0, "Twos": 0, "Threes": 0, "Fours": 0,
                    "Fives": 0, "Sixes": 0, "Bonus": 0, "Total": 0}
    lower_scores = {"Full House": 0, "Small Straight": 0,
                    "Large Straight": 0, "Three of a Kind": 0,
                    "Four of a Kind": 0, "Chance": 0, "Yacht": 0,
                    "Yacht Bonus": 0, "Total": 0, "Final Score": 0}
    upscores = None
    lowscores = None


# yacht scoring functions
def setscore(s_type, s_amt):
    """update player score with selected score"""
    if s_amt == 0:
        s_amt = -1
    if s_type in upper_scores:
        upper_scores[s_type] = s_amt
    elif s_type in lower_scores:
        lower_scores[s_type] = s_amt


def straight(cup, st_type):
    """return rolls point value for small and large straight.  st_type
    check for large over small straight"""
    if 3 in cup and 4 in cup:
        if st_type == "large":
            if 2 in cup and 5 in cup:
                if 1 in cup or 6 in cup:
                    return 40
        elif st_type == "small":
            if (1 in cup and 2 in cup) \
                    or (2 in cup and 5 in cup) \
                    or (5 in cup and 6 in cup):
                return 30
    return 0


def akind(cup, num, k=0):
    """checks for pairs, three of a kind, four of a kind and yacht"""
    scores = {2: 2, 3: sum(cup), 4: sum(cup), 5: 50}
    temp = cup[k]
    cnt = 0
    score = 0
    for i in cup:
        if i == temp:
            cnt += 1
    if cnt >= num != 2:
        score = scores[num]
    elif cnt == num and num == 2:  # prevent invalid Full House
        score = scores[num]
    else:
        if k < (cup.size - 1):
            score = akind(cup, num, k + 1)
    return score


def fullhouse(cup):
    """check that a roll has three of one die value and two of a another"""
    cnt1 = akind(cup, 2)
    cnt2 = akind(cup, 3)
    if cnt1 > 0 and cnt2 > 0:
        return 25
    return 0


def upperscores(cup):
    """returns the available scores for the upper section of the score
    board given a specific roll"""
    temp = Counter(cup.tops())
    upper = {"Ones": temp[1] * 1, "Twos": temp[2] * 2,
             "Threes": temp[3] * 3, "Fours": temp[4] * 4,
             "Fives": temp[5] * 5, "Sixes": temp[6] * 6}
    return upper


def lowerscores(sorteddice):
    """return the available scores for the lower section of the score board
    given a specific roll"""
    lower = {"Chance": sum(sorteddice.tops()),
             "Small Straight": straight(sorteddice,
                                        "small"),
             "Large Straight": straight(sorteddice, "large"),
             "Full House": fullhouse(sorteddice),
             "Three of a Kind": akind(sorteddice, 3),
             "Four of a Kind": akind(sorteddice, 4),
             "Yacht": akind(sorteddice, 5)
             }
    return lower


def getuptotal():
    """get the sum total of the upper section"""
    total = 0
    for i in upper_scores:
        if upper_scores[i] != -1 and i != "Total":
            total += upper_scores[i]
    if total > 63:
        upper_scores["Bonus"] = 35
    upper_scores["Total"] = total


def getlowtotal():
    """get the sum total of the lower section, and the entire board"""
    total = 0
    for i in lower_scores:
        if lower_scores[i] != -1 and (i != "Total" and i != "Final Score"):
            total += lower_scores[i]
    lower_scores["Total"] = total
    lower_scores["Final Score"] = total + upper_scores["Total"]


# pygame functions

def available_scores(screen, diecup, max_score=0):
    """determine what scores are still needed for end game.  max of 0 is
    used for mid-round potential scores.  -1 is passed for end of round"""
    tempup = upperscores(diecup)
    tempdown = lowerscores(diecup)
    upper_x = 325
    upper_y = 205
    lower_x = 450
    lower_y = 205

    upperboxes = []
    lowerboxes = []
    for a_type in tempup:
        if upper_scores[a_type] == 0 and tempup[a_type] > max_score:
            text = FONT18.render("{} = {}".format(a_type, tempup[a_type]),
                                 True, BLACK, GREY)
            rect = text.get_rect()
            rect.left = upper_x
            rect.top = upper_y
            upper_y += 25
            upperboxes.append((rect, a_type, tempup[a_type]))
            screen.blit(text, rect)
    for a_type in tempdown:
        if lower_scores[a_type] == 0 and tempdown[a_type] > max_score:
            text = FONT18.render("{} = {}".format(a_type,
                                                  tempdown[a_type]),
                                 True, BLACK, GREY)
            rect = text.get_rect()
            rect.left = lower_x
            rect.top = lower_y
            lower_y += 25
            lowerboxes.append((rect, a_type, tempdown[a_type]))
            screen.blit(text, rect)
    return upperboxes, lowerboxes


def draw_die(screen, value, pos, diecolor=WHITE, pipcolor=BLACK):
    """pygame integration function; draws dice on screen"""
    die_x, die_y, temp = pos
    rect = pygame.draw.rect(screen, diecolor, (die_x, die_y, 50, 50))
    if value == 1 or value == 3 or value == 5:
        pygame.draw.circle(screen, pipcolor, (die_x + 25, die_y + 25), 5)
    if value != 1:
        pygame.draw.circle(screen, pipcolor, (die_x + 13, die_y + 13), 5)
        pygame.draw.circle(screen, pipcolor, (die_x + 38, die_y + 38), 5)
    if value > 3:
        pygame.draw.circle(screen, pipcolor, (die_x + 13, die_y + 38), 5)
        pygame.draw.circle(screen, pipcolor, (die_x + 38, die_y + 13), 5)
    if value == 6:
        pygame.draw.circle(screen, pipcolor, (die_x + 13, die_y + 26), 5)
        pygame.draw.circle(screen, pipcolor, (die_x + 38, die_y + 26), 5)
    return die_x, die_y, rect


def add_text(screen, rect, score, font, txtcolor):
    """pygame integration function.  adds scores to scoreboard"""
    x, y, wid, lent = rect
    if score == -1:
        score = 0
    text = font.render(str(score), True, txtcolor, GREY)
    text_rect = text.get_rect()
    text_rect.center = ((wid // 2) + x, (lent // 2) + y)
    screen.blit(text, text_rect)


def get_color(currentscore, previousscore, index):
    """return text color; when score is first added to card,
    will flash red, then draw black thereafter"""
    if currentscore[index] != previousscore[index]:
        previousscore[index] = currentscore[index]
        txt_color = RED
    else:
        txt_color = BLACK
    return txt_color


def draw_score(screen):
    """pygame integration function.  draw scoreboard"""
    global lastupper, lastlower
    upper_text = ("UPPER", "SCORES", "Ones", "Fours", "Twos", "Fives",
                  "Threes", "Sixes", "Bonus", "Total")
    lower_text = ("LOWER SCORES", "Three of a Kind", "Four of a Kind",
                  "Full House", "Small Straight", "Large Straight",
                  "Chance", "Yacht", "Yacht Bonus", "Total",
                  "Final Score")
    how_to_score = ("sum of dice", "sum of dice", "25", "30", "40",
                    "sum of dice", "50", "add'l 100")
    pygame.draw.rect(screen, BLACK, (10, 15, 300, 417))
    pygame.draw.rect(screen, WHITE, (15, 20, 290, 407))
    
    x_cor = 50
    y_cor = 35

    line_x_cor1 = 15
    line_x_cor2 = 305
    box_y_cor = 50

    box_len = 35
    box_wid = 25

    left_box_cor = 120
    right_box_cor = 270

    lower_x_cor = 75

    lower_line_y_cor = 150
    lower_line_y_cor_cnst = lower_line_y_cor

    final_line_x = 155
    final_line_y1 = 50
    final_line_y2 = 150
    final_box_y = 175
    cnt = 0

    for text in upper_text:
        line = FONT20.render(text, True, BLACK, WHITE)
        rect = line.get_rect()
        rect.center = (x_cor, y_cor)
        cnt += 1
        if cnt % 2 == 0:
            x_cor = 50
            y_cor += 26
        else:
            x_cor = 200
        screen.blit(line, rect)

    for i in range(4):
        boxes = {1: ("Ones", "Fours"), 2: ("Twos", "Fives"),
                 3: ("Threes", "Sixes"), 4: ("Bonus", "Total")}
        left = boxes[i + 1][0]
        right = boxes[i + 1][1]
        txt_color = get_color(upper_scores, lastupper, left)
        add_text(screen, pygame.draw.rect(screen, GREY,
                                          (left_box_cor, box_y_cor,
                                           box_len, box_wid)),
                 upper_scores[left], FONT20, txt_color)
        txt_color = get_color(upper_scores, lastupper, right)
        add_text(screen, pygame.draw.rect(screen, GREY,
                                          (right_box_cor, box_y_cor,
                                           box_len, box_wid)),
                 upper_scores[right], FONT20, txt_color)
        pygame.draw.line(screen, BLACK, (line_x_cor1, box_y_cor),
                         (line_x_cor2, box_y_cor))
        box_y_cor += 25

    subcat_y = y_cor + 25

    for text in lower_text:
        line = FONT20.render(text, True, BLACK, WHITE)
        rect = line.get_rect()
        rect.center = (lower_x_cor, y_cor)
        rect.left = 20
        y_cor += 25
        screen.blit(line, rect)

    for text in how_to_score:
        line = FONT16.render(text, True, BLACK, WHITE)
        rect = line.get_rect()
        rect.center = (lower_x_cor, subcat_y)
        rect.left = 175
        subcat_y += 25
        screen.blit(line, rect)

    boxes = {1: "Three of a Kind", 2: "Four of a Kind", 3: "Full House",
             4: "Small Straight", 5: "Large Straight", 6: "Chance",
             7: "Yacht", 8: "Yacht Bonus",  9: "Total",
             10: "Final Score"}

    for i in range(10):
        score = boxes[i+1]
        txt_color = get_color(lower_scores, lastlower, score)

        add_text(screen, pygame.draw.rect(screen, GREY, (right_box_cor,
                                                         final_box_y,
                                                         box_len,
                                                         box_wid)),
                 lower_scores[score], FONT20, txt_color)
        pygame.draw.line(screen, BLACK, (line_x_cor1, lower_line_y_cor),
                         (line_x_cor2, lower_line_y_cor))
        lower_line_y_cor += 25
        final_box_y += 25

    pygame.draw.line(screen, BLACK, (line_x_cor1, lower_line_y_cor),
                     (line_x_cor2,
                      lower_line_y_cor))
    pygame.draw.line(screen, BLACK, (line_x_cor1, lower_line_y_cor_cnst),
                     (line_x_cor2, lower_line_y_cor_cnst), 3)
    pygame.draw.line(screen, BLACK, (final_line_x, final_line_y1),
                     (final_line_x, final_line_y2))


def print_scores(screen, scores):
    """pygame integration function.  clear score choices"""
    if scores:
        for i in scores:
            pygame.draw.rect(screen, GREY, i[0])


def refresh_dice(cup, screen, die_array):
    """pygame integration function

    prevent old roll from displaying when a new round starts."""
    if cup.rolls_left == 3:
        for die in range(5):
            dice = die + 1
            draw_die(screen, dice, die_array[die], BLACK, WHITE)
    else:
        for die in range(5):
            dice = cup[die]
            draw_die(screen, dice, die_array[die], dice.held_color)


def instructions():
    """text for instructions of game, then call function to
    print it to the screen"""
    inst = ("Instructions:",  "1: Roll the die to collect points.",
            "2: Hold 0-4 dice and roll again, up to twice more",
            "3: Choose potential points from the right hand list",
            "4: Try to maximize your score by getting the upper"
            "score bonus.", "__",
            "__", "PRESS 'Q' TO RETURN TO GAME")
    Main.blit_instr(inst)


def play_yacht(screen, event, game_in_progress, button, die_array,
               button_flag, cup):
    """control clicks on die and button and handle screen updating"""
    global upscores, lowscores, buttontxt
    draw_score(screen)
    refresh_dice(cup, screen, die_array)
    screen.blit(buttontxt, button)
    for die in range(5):
        if event.type == MOUSEBUTTONUP and \
                die_array[die][2].collidepoint(event.pos):
            if cup.is_held(die):
                cup.release_hold(die)
            else:
                cup.hold(die)
            refresh_dice(cup, screen, die_array)
    for score in upscores:
        score_rect, score_type, score_amount = score
        if event.type == MOUSEBUTTONUP and \
                score_rect.collidepoint(event.pos):
            setscore(score_type, score_amount)
            getuptotal()
            getlowtotal()
            draw_score(screen)
            buttontxt = FONT50.render("New Round", True, WHITE, RED)
            button = pygame.draw.rect(screen, GREY, (
                                      324, 124, 300, 52))
            screen.blit(buttontxt, button)
            button_flag = 3
            print_scores(screen, upscores)
            print_scores(screen, lowscores)
            upscores, lowscores = available_scores(screen, cup)
            refresh_dice(cup, screen, die_array)
            print_scores(screen, upscores)
            print_scores(screen, lowscores)
    for score in lowscores:
        score_rect, score_type, score_amount = score
        if event.type == MOUSEBUTTONUP and \
                score_rect.collidepoint(event.pos):
            setscore(score_type, score_amount)
            getlowtotal()
            draw_score(screen)
            buttontxt = FONT50.render("New Round", True, WHITE, RED)
            button = pygame.draw.rect(screen, GREY, (
                            324, 124, 300, 52))
            screen.blit(buttontxt, button)
            button_flag = 3
            print_scores(screen, upscores)
            print_scores(screen, lowscores)
            upscores, lowscores = available_scores(
                                    screen,
                                    cup)
            refresh_dice(cup, screen, die_array)
            print_scores(screen, upscores)
            print_scores(screen, lowscores)
    if event.type == MOUSEBUTTONUP and\
            button.collidepoint(event.pos):
        button_flag = button_press(screen, die_array, cup, button_flag)

    return game_in_progress, button_flag


def button_press(screen, die_array, cup, button_flag):
    """determine what to do when the main button is pressed
    based on where the game is in a round"""
    global upscores, lowscores, buttontxt
    if button_flag == 2:
        player1_dicecup.roll()
        player1_dicecup.sort()
        print_scores(screen, upscores)
        print_scores(screen, lowscores)
        upscores, lowscores = available_scores(
            screen,
            cup)
        refresh_dice(cup, screen, die_array)
        if cup.rolls_left == 0:
            buttontxt = FONT50.render("Pick Score", True, WHITE, RED)
            button_flag = 4
            button = pygame.draw.rect(screen, GREY,
                                      (324, 124, 300, 52))
            screen.blit(buttontxt, button)
        else:
            buttontxt = FONT50.render("Roll", True, WHITE, RED)
            button_flag = 2
            button = pygame.draw.rect(screen, GREY, (324, 124,
                                                     300, 52))
            screen.blit(buttontxt, button)
    elif button_flag == 3:
        cup.end_turn()
        buttontxt = FONT50.render("Roll", True, WHITE, RED)
        print_scores(screen, upscores)
        print_scores(screen, lowscores)
        upscores, lowscores = available_scores(
            screen,
            cup)
        print_scores(screen, upscores)
        print_scores(screen, lowscores)
        refresh_dice(cup, screen, die_array)
        button_flag = 2
        button = pygame.draw.rect(screen, GREY, (
            324, 124, 300, 52))
        screen.blit(buttontxt, button)
    if button_flag == 4:
        print_scores(screen, upscores)
        print_scores(screen, lowscores)
        upscores, lowscores = \
            available_scores(screen, cup, -1)
    return button_flag


def start_game(screen, event, progress, button, die_array, button_flag):
    """update basic variables needed for the game"""
    global upscores, lowscores, player1_dicecup, buttontxt
    if event.type == MOUSEBUTTONDOWN:
        if button.collidepoint(event.pos):
            player1_dicecup = YatzeeRoll()
            player1_dicecup.sort()
            progress = True
            refresh_dice(player1_dicecup, screen, die_array)
            button = pygame.draw.rect(screen, GREY, (
                        324, 124, 300, 52))
            buttontxt = FONT50.render("Roll", True, WHITE, RED)
            button_flag = 2
            screen.blit(buttontxt, button)
            upscores, lowscores = \
                available_scores(screen, player1_dicecup)
    return progress, button_flag

                                    
def new_game(screen, independent=True):
    """Start a new game"""
    global upper_scores, lower_scores, upscores, lowscores, buttontxt
    pygame.init()
    reset_yacht_globals()
    Main.resetglobals()
    screen.fill(GREY)
    pygame.display.set_caption("Yacht")
    game_in_progress = False

    menu_rect, instr_rect = Main.menu_bar()
    die_array = [None, None, None, None, None]
    die_x = 325
    die_y = 30
    for i in range(5):
        die_array[i] = draw_die(screen, i + 1, (die_x, die_y, None),
                                BLACK, WHITE)
        die_x += 60
    end_game = False
    buttontxt = FONT50.render("New Game", True, WHITE, RED)
    button_flag = 1
    button = pygame.draw.rect(screen, GREY, (324, 124, 300, 52))
    screen.blit(buttontxt, button)
    draw_score(screen)
    while True:
        if not end_game:
            end_game = game_over()
            getuptotal()
            getlowtotal()
            for event in pygame.event.get():
                if event.type == QUIT:
                    saved_game = shelve.open("SavedGame")
                    saved_game['Story_Mode_Finished'] = 3
                    # save location story mode
                    saved_game.close()
                    pygame.quit()
                if event.type == MOUSEBUTTONUP and \
                        menu_rect.collidepoint(event.pos):
                    Main.menu()
                elif event.type == MOUSEBUTTONUP and \
                        instr_rect.collidepoint(event.pos):
                    instructions()
                    screen.fill(GREY)
                    menu_rect, instr_rect = Main.menu_bar()
                    draw_score(screen)
                    upscores, lowscores = available_scores(
                                    screen,
                                    player1_dicecup)
                    try:
                        refresh_dice(player1_dicecup, screen,
                                     die_array)
                    except UnboundLocalError:
                        for die in range(5):
                            dice = die + 1
                            draw_die(screen, dice, die_array[die],
                                     BLACK, WHITE)
                if game_in_progress:
                    game_in_progress, button_flag = \
                        play_yacht(screen, event, game_in_progress,
                                   button, die_array, button_flag,
                                   player1_dicecup)
                else:
                    game_in_progress, button_flag = \
                        start_game(screen, event, game_in_progress, button,
                                   die_array, button_flag)
        else:
            if independent:
                finish(screen, menu_rect, instr_rect)
            else:
                if lower_scores["Final Score"] < 200:
                    return True
                return False
                    
        pygame.display.flip()


# end game functions

def finish(screen, menu_rect, instr_rect):
    """end the game"""
    endgame_box("GAME OVER!  You got {} points!  "
                " New Game? Press"
                " 'Y' or 'N'".format
                (lower_scores["Final Score"]),
                screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            saved_game = shelve.open("SavedGame")
            saved_game['Story_Mode_Finished'] = 3
            # save location story mode
            saved_game.close()
            pygame.quit()
        if event.type == KEYUP and event.key == K_y:
            new_game(screen)
        elif (event.type == KEYUP and event.key == K_n) \
                or (event.type == MOUSEBUTTONUP
                    and menu_rect.collidepoint(event.pos)):
            Main.menu()
        elif event.type == MOUSEBUTTONUP and \
                instr_rect.collidepoint(event.pos):
            instructions()
            new_game(screen)


def game_over():
    """check for game over"""
    for score in upper_scores:
        if upper_scores[score] == 0 and score != "Bonus":
            return False
    for score in lower_scores:
        if lower_scores[score] == 0 and score != "Yacht Bonus":
            return False
    return True


def endgame_box(given_text, a_screen):
    """end game text box"""
    text_list = []
    temp_text = ""
    next_line = 325
    warn_location = (320, 325, 220, 125)
    text_center = 485
    while len(given_text) > 0:
        temp_text += given_text[0]
        try:
            given_text = given_text[1:]
            if len(temp_text) >= 10 and temp_text[-1] == " ":
                text_list.append(temp_text)
                temp_text = ""
        except IndexError:
            pass
    temp_text += given_text
    text_list.append(temp_text)
    frame = [""] * len(text_list)
    rect = [""] * len(text_list)
    pygame.draw.rect(a_screen, GREY, pygame.Rect(warn_location))
    for line in range(len(text_list)):

        frame[line] = FONT20.render(text_list[line], True, RED, GREY)
        rect[line] = frame[line].get_rect()
        rect[line].center = (text_center, next_line)
        a_screen.blit(frame[line], rect[line])
        next_line += 20
