import pygame, sys
from audio import *
from button import Button
from config import *
from world import World
from player import Player
from lava import Lava
from coin import Coin
from pintu import Pintu


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("MasBro Jumping 2D")
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        #load gambar
        self.sky_img = pygame.image.load('img/sky.png')
        self.sky_img = pygame.transform.scale(self.sky_img, SCREEN_SIZE)

        self.jamur_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.pintu_group = pygame.sprite.Group()
        self.bendera_group = pygame.sprite.Group()
        self.prajurit_group = pygame.sprite.Group()

        self.level = 3
        self.world = World(PETA_DUNIA[self.level - 1], [self.jamur_group, self.lava_group, self.coin_group, self.pintu_group, self.bendera_group, self.prajurit_group], 0)

        self.restart_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 'restart_btn')
        self.start_button = Button((SCREEN_WIDTH // 2) - 150, SCREEN_HEIGHT // 2, 'start_btn')
        self.exit_button = Button((SCREEN_WIDTH // 2) + 150, SCREEN_HEIGHT // 2, 'exit_btn')

        self.coin_img = pygame.image.load('img/coin.png').convert_alpha()
        self.coin_img = pygame.transform.scale(self.coin_img, (FONT_SIZE, FONT_SIZE))
        self.coin_rect = self.coin_img.get_rect(topleft = (GAP, GAP))

        # State
        self.GAME_OVER = 0
        self.MAIN_MENU = 1
        self.LEVEL_OVER = 0

        self.font = pygame.font.SysFont('consolas', FONT_SIZE)
        self.font_menang = pygame.font.SysFont('consolas', FONT_SIZE)
        
        self.gameover_image = pygame.image.load('img/Ending.png').convert_alpha()
        self.gameover_image = pygame.transform.scale(self.gameover_image, SCREEN_SIZE)

        background_music()


    def draw_text(self, text, text_col, x=0, y=0, center=False, centertop = False):
        img = self.font.render(text, True, text_col)
        if center:
            img_rect = img.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(img, img_rect)
        elif centertop:
            img_rect = img.get_rect(center = (SCREEN_WIDTH / 2, GAP))
            self.screen.blit(img, img_rect)
        else:
            self.screen.blit(img, (x, y))

    def draw_grid(self):
        for line in range(int(SCREEN_WIDTH / TILE_WIDTH) + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (0, line * TILE_WIDTH), (SCREEN_WIDTH, line * TILE_WIDTH))
            pygame.draw.line(self.screen, (255, 255, 255), (line * TILE_HEIGHT, 0), (line * TILE_HEIGHT, SCREEN_HEIGHT))
        
    def run(self):
        while True:
            self.screen.blit(self.sky_img, (0, 0))
            # self.draw_grid()
            # print(self.world.tile_list)

            if self.MAIN_MENU:
                if self.exit_button.draw():
                    pygame.quit()
                    sys.exit()
                if self.start_button.draw():
                    self.MAIN_MENU = 0
                    start_sfx()
                    self.start = pygame.time.get_ticks()
            elif self.LEVEL_OVER == 0:
                    

                self.world.draw()
                if self.GAME_OVER == 0:
                    self.jamur_group.update()
                self.jamur_group.draw(self.screen)
                self.lava_group.draw(self.screen)
                self.pintu_group.draw(self.screen)
                self.bendera_group.draw(self.screen)
                self.prajurit_group.draw(self.screen)
                
                for coin in self.coin_group:
                    if not coin.obtained:
                        self.screen.blit(coin.image, coin.rect)
                #restart button 
                self.GAME_OVER, self.LEVEL_OVER = self.world.player.update(self.GAME_OVER, self.LEVEL_OVER)
                if self.GAME_OVER == -1:
                    if self.restart_button.draw():
                        self.world.player.reset()
                        self.GAME_OVER = 0
                    
                if self.LEVEL_OVER == 1:
                    # self.draw_text('You Win!', 'black', center=True)
                    self.screen.blit(self.gameover_image, (0, 0))
                elif self.LEVEL_OVER == 0:
                    self.time = pygame.time.get_ticks() - self.start

                if self.world.player.next_level:
                    self.level += 1
                    self.jamur_group.empty()
                    self.lava_group.empty()
                    self.coin_group.empty()
                    self.pintu_group.empty()
                    self.prajurit_group.empty()
                    #self.bendera_group.empty()
                    score = self.world.player.score
                    self.world = World(PETA_DUNIA[self.level - 1], [self.jamur_group, self.lava_group, self.coin_group, self.pintu_group, self.bendera_group, self.prajurit_group], score)


            # Score
                self.screen.blit(self.coin_img, self.coin_rect)
                self.draw_text(f'X {self.world.player.score}', 'black', GAP + self.coin_rect.right, self.coin_rect.y + 3)
                self.draw_text(f'Time: {self.time/1000}', 'black', centertop=True)

            elif self.LEVEL_OVER == 1:
                self.screen.blit(self.gameover_image, (0, 0))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    pygame.quit()
                    sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # if self.GAME_OVER == -1
            
            pygame.display.update()
            self.clock.tick(DEFAULT_FPS)
            #print(self.clock.get_fps())
