import pygame
from pygame import mixer

pygame.mixer.init()

def start_sfx():
    sound = pygame.mixer.Sound('audio/start.wav')
    sound.set_volume(2)
    sound.play()

def background_music():
    pygame.mixer.music.load('audio/background.wav')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

def dead_sfx():
    sound = pygame.mixer.Sound('audio/mati.wav')
    sound.set_volume(10)
    sound.play()