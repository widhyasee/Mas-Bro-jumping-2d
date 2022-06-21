import pygame
from config import *

class Pintu(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pintu.png')
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - TILE_HEIGHT
        self.move_direction = 1
        self.move_counter = 0