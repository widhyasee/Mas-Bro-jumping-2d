import pygame
from coin import Coin
from config import *
from enemy import Enemy, Enemy2
from lava import Lava
from pintu import Pintu
from player import Player
from bendera import Bendera

class World:
    def __init__(self, data, group, score):
        self.tile_list = []
        self.screen = pygame.display.get_surface()
        
        #load pinggiran map
        self.border_tanah = pygame.image.load('img/wall.png')
        self.grass = pygame.image.load('img/grass.png')
        self.water = pygame.image.load('img/air.png')
        self.dirt = pygame.image.load('img/dirt.png')
        self.lava = pygame.image.load('img/lava.png')
        self.coin = pygame.image.load('img/coin.png')
        self.pintu = pygame.image.load('img/pintu.png')
        self.bendera = pygame.image.load('img/bendera.png')
        self.prajurit = pygame.image.load('img/prajurit.png')
        
        self.jamur_group = group[0]
        self.lava_group = group[1]
        self.coin_group = group[2]
        self.pintu_group = group[3]
        self.bendera_group = group[4]
        self.prajurit_group = group[5]


        self.row_count = 0
        for row in data:
            self.col_count = 0
            for tile in row:
                if tile == 1:
                    self.img = pygame.transform.scale(self.border_tanah, TILE_SIZE)
                    self.img_rect = self.img.get_rect()
                    self.img_rect.x = self.col_count * TILE_WIDTH
                    self.img_rect.y = self.row_count * TILE_HEIGHT
                    self.tile = (self.img, self.img_rect)
                    self.tile_list.append(self.tile)
                elif tile == 2:
                    self.img = pygame.transform.scale(self.grass, TILE_SIZE)
                    self.img_rect = self.img.get_rect()
                    self.img_rect.x = self.col_count * TILE_WIDTH
                    self.img_rect.y = self.row_count * TILE_HEIGHT
                    self.tile = (self.img, self.img_rect)
                    self.tile_list.append(self.tile)
                elif tile == 3:
                    self.lava = Lava(self.col_count * TILE_WIDTH, self.row_count * TILE_HEIGHT)
                    self.lava_group.add(self.lava)
                elif tile == 4: #dirt
                    self.img = pygame.transform.scale(self.dirt, TILE_SIZE)
                    self.img_rect = self.img.get_rect()
                    self.img_rect.x = self.col_count * TILE_WIDTH
                    self.img_rect.y = self.row_count * TILE_HEIGHT
                    self.tile = (self.img, self.img_rect)
                    self.tile_list.append(self.tile)
                elif tile == 5:
                    self.jamur = Enemy(self.col_count * TILE_WIDTH, self.row_count * TILE_HEIGHT)
                    self.jamur_group.add(self.jamur)
                elif tile == 6:
                    self.coin = Coin(self.col_count * TILE_WIDTH + (TILE_WIDTH // 2), self.row_count * TILE_HEIGHT + (TILE_HEIGHT // 2))
                    self.coin_group.add(self.coin)
                elif tile == 7:
                    self.pintu = Pintu(self.col_count * TILE_WIDTH + (TILE_WIDTH // 2), self.row_count * TILE_HEIGHT + (TILE_HEIGHT // 2))
                    self.pintu_group.add(self.pintu)
                elif tile == 8:
                    self.player = Player(self.col_count * TILE_WIDTH, self.row_count * TILE_HEIGHT, self, [self.jamur_group, self.lava_group, self.coin_group, self.pintu_group, self.bendera_group, self.prajurit_group], score)
                elif tile == 9:
                    self.bendera = Bendera(self.col_count * TILE_WIDTH + (TILE_WIDTH // 2), self.row_count * TILE_HEIGHT + (TILE_HEIGHT // 2))
                    self.bendera_group.add(self.bendera)
                elif tile == 10:
                    self.prajurit = Enemy2(self.col_count * TILE_WIDTH, self.row_count * TILE_HEIGHT)
                    self.prajurit_group.add(self.prajurit)
                self.col_count += 1
            self.row_count += 1

    def draw(self):
        for tile in self.tile_list:
            self.screen.blit(tile[0], tile[1])
            # pygame.draw.rect(self.screen, (255, 255, 255), tile[1], 2)
        