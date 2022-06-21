import pygame
from config import * 
class Button() :
    def __init__(self, x, y, image) :
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load(f'img/{image}.png')
        self.image = pygame.transform.scale(self.image, BUTTON_SIZE)
        self.rect = self.image.get_rect(center = (x, y))
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        self.screen.blit(self.image, self.rect)

        return action
