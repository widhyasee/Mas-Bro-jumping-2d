import pygame
from config import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/coin.png')
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH // 2, TILE_HEIGHT // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.obtained = False


