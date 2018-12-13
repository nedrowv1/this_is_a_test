import random
import pygame
from pygame.locals import *
import sys
import Grandmas_Game_Closet as Main
import shelve


# colors
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
ROYAL = (80, 45, 114)
CREAM = (255, 222, 163)

GALLOWSTOP = (225, 30, 150, 10)
GALLOWSPOLE = (365, 30, 10, 250)
GALLOWSBOTTOM = (225, 280, 250, 15)
ROPE = (230, 30, 2, 20)
HEADCENTER = (230, 80)
HEADRADIUS = 30
EYERADIUS = 3
EYE_Y = 68
LEFTEYE_X = 220
RIGHTEYE_X = 240
WINWIDTH = 640
WINHEIGHT = 480
INVALID_Y = 50
INVALID_X = 525


def reset_hangman_globals(screen):
    """reset global variables for handman"""
    global FPS
    global BGCOLOR, FPSCLOCK
    FPS = 60
    BGCOLOR = ROYAL
    FPSCLOCK = pygame.time.Clock()
    screen.fill(BGCOLOR)


def create_gallows(screen):
    """draw the gallows"""
    pygame.draw.rect(screen, CREAM, GALLOWSTOP)
    pygame.draw.rect(screen, CREAM, GALLOWSPOLE)
    pygame.draw.rect(screen, CREAM, GALLOWSBOTTOM)
    pygame.draw.rect(screen, TAN, ROPE)


def head(screen):
    """draw the head of the condemned figure"""
    pygame.draw.circle(screen, LIGHTSKIN, HEADCENTER, HEADRADIUS)
    pygame.draw.circle(screen, BLACK, (LEFTEYE_X, EYE_Y), EYERADIUS)
    pygame.draw.circle(screen, BLACK, (RIGHTEYE_X, EYE_Y), EYERADIUS)
    pygame.display.flip()
    pygame.draw.arc(screen, RED, (200, 90, 50, 25), 1, 2, 1)
    pygame.draw.arc(screen, BLACK, (200, 50, 60, 60), 0, 3, 6)


def body(screen):
    """draw the body of the condemned figure"""
    pygame.draw.ellipse(screen, DARKGREEN, (200, 110, 60, 100), 0)


def leftleg(screen):
    """draw the left left of the condemned figure"""
    pygame.draw.ellipse(screen, DARKGREEN, (210, 200, 20, 50))
    pygame.draw.circle(screen, LIGHTSKIN, (220, 250), 10)


def rightleg(screen):
    """draw the right leg of the condemned figure"""
    pygame.draw.ellipse(screen, DARKGREEN, (230, 200, 20, 50))
    pygame.draw.circle(screen, LIGHTSKIN, (240, 250), 10)


def leftarm(screen):
    """draw the left arm of the condemned figure"""
    pygame.draw.ellipse(screen, DARKGREEN, (170, 110, 50, 20))
    pygame.draw.circle(screen, LIGHTSKIN, (170, 120), 10)


def rightarm(screen):
    """draw the right arm of the condemned figure"""
    pygame.draw.ellipse(screen, DARKGREEN, (240, 110, 50, 20))
    pygame.draw.circle(screen, LIGHTSKIN, (290, 120), 10)


def dead(a_word, define, screen, standalone):
    """lost the game.  drawing won't show in story mode"""
    pygame.draw.circle(screen, LIGHTSKIN, HEADCENTER, HEADRADIUS)
    pygame.draw.line(screen, BLACK, (220, 70), (215, 65))
    pygame.draw.line(screen, BLACK, (215, 70), (220, 65))
    pygame.draw.line(screen, BLACK, (235, 70), (240, 65))
    pygame.draw.line(screen, BLACK, (240, 70), (235, 65))
    pygame.draw.arc(screen, RED, (200, 90, 50, 25), 1, 2, 1)
    pygame.draw.arc(screen, BLACK, (200, 50, 60, 60), 0, 3, 6)
    word_font = pygame.font.Font('freesansbold.ttf', 25)
    word_print = word_font.render("YOU LOST x_x", True, RED, BLACK)
    invalid_rect = word_print.get_rect()
    invalid_rect.center = (237, 111)
    screen.blit(word_print, invalid_rect)
    word_print = word_font.render("word: {}".format(a_word), True,
                                  RED, BLACK)
    invalid_rect = word_print.get_rect()
    invalid_rect.center = (237, 141)
    screen.blit(word_print, invalid_rect)
    word_print = word_font.render("definition: {}".format(define),
                                  True, RED, BLACK)
    invalid_rect = word_print.get_rect()
    invalid_rect.center = (237, 171)
    screen.blit(word_print, invalid_rect)
    if standalone:
        word_print = word_font.render("Play Again?  'Y' or 'N'",
                                      True, RED, BLACK)
        invalid_rect = word_print.get_rect()
        invalid_rect.center = (237, 201)
        screen.blit(word_print, invalid_rect)
        for event in pygame.event.get():
            print(event.type)
            if event.type == KEYUP and event.key == K_y:
                new_game(screen)
            elif event.type == KEYUP and event.key == K_n:
                Main.menu()
            elif event.type == QUIT or (event.type == KEYUP and
                                        (event.key == K_ESCAPE or
                                         event.key == K_q)):
                saved_game = shelve.open("SavedGame")
                saved_game['Story_Mode_Finished'] = 2
                # save location story mode
                saved_game.close()
                pygame.quit()
                sys.exit()
    pygame.display.update()


def get_key(pressed):
    """determine what key was pressed"""
    alphadict = {K_a: 'a', K_b: 'b', K_c: 'c', K_d: 'd', K_e: 'e',
                 K_f: 'f', K_g: 'g', K_h: 'h', K_i: 'i', K_j: 'j',
                 K_k: 'k', K_l: 'l', K_m: 'm', K_n: 'n', K_o: 'o',
                 K_p: 'p', K_q: 'q', K_r: 'r', K_s: 's', K_t: 't',
                 K_u: 'u', K_v: 'v', K_w: 'w', K_x: 'x', K_y: 'y',
                 K_z: 'z'}
    try:
        return alphadict[pressed]
    except KeyError:
        return "_"


def print_word(a_word, screen):
    """print the word, and blanks on the screen"""
    global WORD_RECT
    letters = ""
    for i in range(len(a_word)):
        letters += a_word[i]
        if i != len(a_word) - 1:
            letters += " "
    word_font = pygame.font.Font('freesansbold.ttf', 25)
    word_print = word_font.render(letters, True, CREAM, BGCOLOR)
    WORD_RECT = word_print.get_rect()
    WORD_RECT.center = (260, 340)
    screen.blit(word_print, WORD_RECT)


def has_won(a_list, a_word, define, screen, standalone):
    """the word was guessed.  will not print to screen in story mode"""
    if "_" not in a_list:
        word_font = pygame.font.Font('freesansbold.ttf', 25)
        word_print = word_font.render("YOU WON ^_^", True, GREEN, BLACK)
        invalid_rect = word_print.get_rect()
        invalid_rect.center = (237, 111)
        screen.blit(word_print, invalid_rect)
        word_print = word_font.render("word:{}".format(a_word),
                                      True, GREEN, BLACK)
        invalid_rect = word_print.get_rect()
        invalid_rect.center = (237, 141)
        screen.blit(word_print, invalid_rect)
        word_print = word_font.render("definition:{}".format(define),
                                      True, GREEN, BLACK)
        invalid_rect = word_print.get_rect()
        invalid_rect.center = (237, 171)
        screen.blit(word_print, invalid_rect)
        if standalone:
            word_print = word_font.render("Play Again? 'Y' or 'N'",
                                          True, GREEN, BLACK)
            invalid_rect = word_print.get_rect()
            invalid_rect.center = (237, 201)
            screen.blit(word_print, invalid_rect)
        return True
    return False


def guilty(body_parts, a_word, define, screen, ind):
    """determine what body part should be drawn"""
    if body_parts == 1:
        head(screen)
    elif body_parts == 2:
        body(screen)
    elif body_parts == 3:
        leftleg(screen)
    elif body_parts == 4:
        rightleg(screen)
    elif body_parts == 5:
        leftarm(screen)
    elif body_parts == 6:
        rightarm(screen)
    else:
        dead(a_word, define, screen, ind)
        return True
    return False


def print_invalid(invalid, screen):
    """print letters guessed that weren't in word"""
    global INVALID_Y
    for letter in invalid:
        word_font = pygame.font.Font('freesansbold.ttf', 25)
        word_print = word_font.render(letter, True, RED, ROYAL)
        invalid_rect = word_print.get_rect()
        invalid_rect.center = (INVALID_X, INVALID_Y)
        screen.blit(word_print, invalid_rect)
        INVALID_Y += 40
    INVALID_Y = 50


def update(letter, a_word, a_list):
    """update the printed version of the word"""
    for let in range(len(a_word)):
        if a_word[let] == letter:
            a_list[let] = letter


def instructions():
    """text of instructions, function call to print to the screen"""
    inst = ("Instructions:", "__", "1: Guess the hidden word", "__",
            "2: Correct letters appear in the word below the gallows",
            "__", "3: Incorrect letters appear to the right of "
                  "the gallows",
            "__", "4:You have seven chances to save the condemned man "
            "from being hanged.", "__", "__",
            "PRESS 'Q' TO RETURN TO GAME")
    Main.blit_instr(inst)


def hangman(a_word, define, screen, ind):
    """main hangman logic"""
    won = False
    lost = False
    pygame.init()
    create_gallows(screen)
    letter_list = ['_'] * len(a_word)
    print_word(letter_list, screen)
    invalidletters = ""
    menu_rect, instr_rect = Main.menu_bar()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                saved_game = shelve.open("SavedGame")
                saved_game['Story_Mode_Finished'] = 2
                # save location story mode
                saved_game.close()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP and \
                    menu_rect.collidepoint(event.pos):
                Main.menu()
            elif event.type == MOUSEBUTTONUP and \
                    instr_rect.collidepoint(event.pos):
                instructions()
                reset_hangman_globals(screen)
                Main.menu_bar()
                create_gallows(screen)
                print_word(letter_list, screen)
                print_invalid(invalidletters, screen)
                guilty(len(invalidletters), a_word, define, screen, ind)
            if not won and not lost:
                if event.type == KEYUP:
                    letter = get_key(event.key)
                    if letter == "_":
                        pass
                    elif letter in a_word:
                        update(letter, a_word, letter_list)
                        pygame.draw.rect(screen, BGCOLOR, WORD_RECT)
                        print_word(letter_list, screen)
                        won = has_won(letter_list, a_word, define, screen,
                                      ind)
                    elif letter not in invalidletters:
                        invalidletters += letter
                        lost = guilty(len(invalidletters), a_word,
                                      define, screen, ind)
                        print_invalid(invalidletters, screen)
            elif event.type == KEYUP:
                if event.key == K_y:
                    new_game(screen)
                elif event.key == K_n:
                    Main.menu()
        pygame.display.flip()
        if won:
            return False
        if lost:
            return True


def new_game(screen, independent=True):
    """start a new game"""
    pygame.init()
    wordlist = {'abode': 'a home', 'access': 'an outburst of an emotion',
                'adieu': 'goodbye', 'afar': 'at a distance',
                'apace': 'quickly', 'argosy': 'a large merchant ship',
                'arrant': 'utter', 'asunder': 'into pieces',
                'atrabilious': 'melancholy or bad-tempered',
                'aurora': 'the dawn', 'bard': 'a poet', 'barque': 'a boat',
                'bedizen': 'dress gaudily', 'beget': 'produce (a child)',
                'behold': 'see', 'beseech': 'ask urgently and fervently',
                'bestrew': 'scatter', 'betake oneself': 'go to',
                'betide': 'happen', 'betoken': 'be a warning of',
                'blade': 'sword', 'blithe': 'happy',
                'bosky': 'covered by trees or bushes', 'brand': 'a sword',
                'brume': 'mist or fog', 'celerity': 'swiftness',
                'circumvallate': 'surround with a rampart or wall',
                'clarion': 'loud and clear', 'cleave to': 'stick fast to',
                'cockcrow': 'dawn', 'coruscate': 'flash or sparkle',
                'crapulent': 'relating to the drinking of alcohol',
                'crescent': 'growing',
                'darkling': 'relating to growing darkness',
                'dell': 'a small valley', 'dingle': 'a deep wooded valley',
                'divers': 'of varying types', 'Dives': 'a rich man',
                'dolour': 'great sorrow', 'dome': 'a stately building',
                'dulcify': 'sweeten', 'effulgent': 'shining brightly',
                'eld': 'old age', 'eminence': 'a piece of rising ground',
                'empyrean': 'the sky', 'ere': 'before',
                'erne': 'a sea eagle',
                'espy': 'catch sight of', 'ether': 'the clear sky',
                'evanescent': 'quickly fading', 'farewell': 'goodbye',
                'fervid': 'hot or glowing', 'finny': 'relating to fish',
                'firmament': 'the sky', 'flaxen': 'pale yellow',
                'fleer': 'jeer or laugh disrespectfully',
                'flexuous': 'full of bends and curves',
                'fulgent': 'shining brightly',
                'fulguration': 'a flash like lightning',
                'fuliginous': 'sooty; dusky',
                'fulminate': 'explode violently',
                'furbelow': 'adorn with trimmings',
                'gird': 'secure with a belt',
                'glaive': 'a sword', 'gloaming': 'dusk',
                'greensward': 'grassy ground', 'gyre': 'whirl or gyrate',
                'hark': 'listen',
                'horripilation': 'gooseflesh; hair standing on end',
                'hymeneal': 'relating to marriage',
                'ichor': 'blood or a fluid likened to it',
                'illude': 'trick someone',
                'imbrue': 'stain ones hand or sword with blood',
                'impuissant': 'powerless',
                'incarnadine': 'colour (something) crimson',
                'ingrate': 'ungrateful', 'inhume': 'bury',
                'inly': 'inwardly',
                'ire': 'anger', 'isle': 'an island',
                'knell': 'the sound of a bell',
                'lachrymal': 'connected with weeping or tears',
                'lacustrine': 'associated with lakes',
                'lambent': 'softly glowing or flickering',
                'lave': 'wash or wash over', 'lay': 'a song',
                'lea': 'an area of grassy land',
                'lenity': 'kindness or gentleness',
                'lightsome': 'nimble',
                'limn': 'represent in painting or words',
                'lucent': 'shining', 'madding': 'acting madly; frenzied',
                'mage': 'a magician or learned person',
                'malefic': 'causing harm',
                'manifold': 'many and various', 'marge': 'a margin',
                'mead': 'a meadow', 'mephitic': 'foul-smelling',
                'mere': 'a lake or pond', 'moon': 'a month',
                'muliebrity': 'womanliness',
                'nescient': 'lacking knowledge; ignorant', 'nigh': 'near',
                'niveous': 'snowy',
                'nocuous': 'noxious harmful or poisonous',
                'noisome': 'foul-smelling',
                'nymph': 'a beautiful young woman',
                'orb': 'an eye', 'orgulous': 'proud or haughty',
                'pellucid': 'translucent', 'perchance': 'by some chance',
                'perfervid': 'intense and impassioned',
                'perfidious': 'deceitful and untrustworthy',
                'philippic': 'a bitter verbal attack',
                'plangent': 'loud and mournful',
                'plash': 'a splashing sound',
                'plenteous': 'plentiful', 'plumbless': 'extremely deep',
                'poesy': 'poetry',
                'prothalamium': 'a song or poem celebrating a wedding',
                'puissant': 'powerful or influential',
                'pulchritude': 'beauty',
                'purl': 'flow with a babbling sound',
                'quidnunc': 'an inquisitive and gossipy person',
                'realm': 'a kingdom', 'refulgent': 'shining brightly',
                'rend': 'tear to pieces', 'repine': 'be discontented',
                'Rhadamanthine': 'stern and incorruptible in judgement',
                'roundelay': 'a short, simple song with a refrain',
                'rubescent': 'reddening',
                'rutilant': 'glowing or glittering '
                            'with red or golden light',
                'sans': 'without', 'scribe': 'write',
                'sea-girt': 'surrounded by sea',
                'sempiternal': 'everlasting',
                'serpent': 'a snake', 'shade': 'a ghost',
                'ship of the desert': 'a camel',
                'shore': 'country by the sea',
                'slay': 'kill', 'slumber': 'sleep',
                'star-crossed': 'ill-fated', 'steed': 'a horse',
                'stilly': 'still and quiet',
                'storied': 'celebrated in stories', 'strand': 'a shore',
                'Stygian': 'very dark',
                'summer': 'a year of a persons age',
                'supernal': 'relating to the sky or the heavens',
                'susurration': 'a whispering or rustling sound',
                'swain': 'a young lover or suitor', 'sylvan': 'wooded',
                'tarry': 'delay leaving',
                'temerarious': 'rash or reckless',
                'tenebrous': 'dark; shadowy', 'threescore': 'sixty',
                'thrice': 'three times', 'tidings': 'news; information',
                'toilsome': 'involving hard work',
                'tope': 'drink alcohol to excess',
                'travail': 'painful or laborious effort',
                'troublous': 'full of troubles',
                'tryst': 'a rendezvous between lovers',
                'unman': 'deprive of manly qualities',
                'vestal': 'chaste; pure', 'vesture': 'clothing',
                'virescent': 'greenish',
                'viridescent': 'greenish or becoming green',
                'visage': 'a persons face', 'want': 'lack or be short of',
                'wax': 'become larger or stronger',
                'wayfarer': 'a person who travels on foot',
                'wed': 'marry', 'wind': 'blow (a bugle)',
                'without': 'outside',
                'wondrous': 'inspiring wonder', 'wont': 'accustomed',
                'wonted': 'usual', 'wrathful': 'extremely angry',
                'wreathe': 'twist or entwine', 'yon': 'yonder; that',
                'yore': 'of former ties or long ago',
                'youngling': 'a young person or animal',
                'zephyr': 'a soft, gentle breeze'}

    # word list found at:
    # https://en.oxforddictionaries.com/explore/literary-words/

    Main.resetglobals()
    reset_hangman_globals(screen)
    word, definition = random.choice(list(wordlist.items()))
    game_result = hangman(word, definition, screen, independent)
    if not independent:
        print(game_result)
        return game_result, word, definition
