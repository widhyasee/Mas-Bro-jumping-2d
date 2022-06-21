import pygame
from config import *
from audio import *
from coin import Coin

class Player():
    def __init__(self, x, y, world, group, score):
        self.screen = pygame.display.get_surface()
        self.images_right_idle = []
        self.images_left_idle = []
        self.images_right_run = []
        self.images_left_run = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            self.img_right = pygame.image.load(f'img/guy_idle{num}.png').convert_alpha()
            self.img_right = pygame.transform.scale(self.img_right, PLAYER_SIZE)
            self.img_left = pygame.transform.flip(self.img_right, True, False)
            self.images_right_idle.append(self.img_right)
            self.images_left_idle.append(self.img_left)
        for num in range(1, 3):
            self.img_right = pygame.image.load(f'img/guy_run{num}.png').convert_alpha()
            self.img_right = pygame.transform.scale(self.img_right, PLAYER_SIZE)
            self.img_left = pygame.transform.flip(self.img_right, True, False)
            self.images_right_run.append(self.img_right)
            self.images_left_run.append(self.img_left)

        self.image = self.images_right_idle[self.index]
        self.dead_image = pygame.image.load('img/guy_death.png').convert_alpha()
        self.dead_image = pygame.transform.scale(self.dead_image, PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.is_grounded = False
        self.idle = True
        self.direction = 0
        self.world = world
        
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.jamur_group = group[0]
        self.lava_group = group[1]
        self.coin_group = group[2]
        self.pintu_group = group[3]
        self.bendera_group = group[4]
        self.prajurit_group = group[5]
    
        self.level_x = x
        self.level_y = y

        self.score = score
        self.next_level = False
        
        #loadsoundsbackground
        #pygame.mixer.music.load('audio/background.wav')
        #pygame.mixer.music.play(-1, 0.0, 4000)
        
    def reset(self):
        self.index = 0
        self.counter = 0
        self.rect.x = self.level_x
        self.rect.y = self.level_y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.score = 0
        for coin in self.coin_group:
            coin.obtained = False

    def update(self, GAME_OVER, LEVEL_OVER):
        dx = 0
        dy = 0
        walk_cooldown = 5
        if GAME_OVER == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.is_grounded:
                self.vel_y = -PLAYER_JUMP
                self.jumped = True
                self.is_grounded = False
                self.idle = False
            if key[pygame.K_SPACE] == False:
                self.jumped = False
                self.idle = False
            if key[pygame.K_LEFT]:
                dx -= PLAYER_SPEED
                self.counter += 1
                self.direction = -1
                self.idle = False
            if key[pygame.K_RIGHT]:
                dx += PLAYER_SPEED
                self.counter += 1
                self.direction = 1
                self.idle = False
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                self.idle = True
                if self.direction == 1:
                    self.image = self.images_right_idle[self.index]
                if self.direction == -1:
                    self.image = self.images_left_idle[self.index]

            #handle animation
            if not self.idle:
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right_run):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right_run[self.index]
                    if self.direction == -1:
                        self.image = self.images_left_run[self.index]
            elif self.idle:
                if self.counter > walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right_idle):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right_idle[self.index]
                    if self.direction == -1:
                        self.image = self.images_left_idle[self.index]

            # add gravity
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
            self.is_grounded = False

            for tile in self.world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.is_grounded = True

            # check collision with enemy
            if pygame.sprite.spritecollide(self, self.jamur_group, False):
                GAME_OVER = -1
                dead_sfx()

            # check collision with prajurit
            if pygame.sprite.spritecollide(self, self.prajurit_group, False):
                GAME_OVER = -1
                dead_sfx()
            
            # check collision with lava
            if pygame.sprite.spritecollide(self, self.lava_group, False):
                GAME_OVER = -1
                dead_sfx()

                #print(GAME_OVER)
            
            if pygame.sprite.spritecollide(self, self.pintu_group, False):
                self.next_level = True

            if pygame.sprite.spritecollide(self, self.bendera_group, False):
                LEVEL_OVER = 1
            
            # check collision coin
            for coin in self.coin_group:
                if self.rect.colliderect(coin.rect) and not coin.obtained:
                    coin.obtained = True
                    self.score += 1
            
            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            #if self.rect.bottom > SCREEN_HEIGHT:
            #   self.rect.bottom = SCREEN_HEIGHT
            #  dy = 0

        elif GAME_OVER == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

            # draw player onto screen
        self.screen.blit(self.image, self.rect)
        #pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)

        return GAME_OVER, LEVEL_OVER