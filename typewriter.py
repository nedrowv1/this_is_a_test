"""modified from code (c) 2016 sloth.  unlicensed."""

import pygame


class Board(pygame.sprite.Sprite):
    def __init__(self, height, width, bgcolor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(bgcolor)
        self.image.set_colorkey(bgcolor)
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("freesansbold.tff", 18)

    def add(self, letter, pos, txtcolor):
        s = self.font.render(letter, 1, txtcolor)
        self.image.blit(s, pos)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, board, color, hgt=17, wdth=10):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(color)
        self.text_height = hgt
        self.text_width = wdth
        self.rect = self.image.get_rect(topleft=(self.text_width,
                                               self.text_height))
        self.board = board
        self.text = []
        self.color = color
        self.cooldown = 0
        self.cooldowns = {'.': 12,
                        ' ': 5,
                        '\n': 30}

    def write(self, text):
        self.text = list(text)

    def update(self):
        if not self.cooldown and self.text:
            letter = self.text.pop(0)
            if letter == '\n':
                self.rect.move_ip((0, self.text_height))
                self.rect.x = self.text_width
            else:
                self.board.add(letter, self.rect.topleft, self.color)
                self.rect.move_ip((self.text_width, 0))
            self.cooldown = self.cooldowns.get(letter, 8)

        if self.cooldown:
            self.cooldown -= 1
