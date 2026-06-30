import numpy as np
import pygame
import objects

def detect_collision(list_of_object: list = []):
    for i in list_of_object:

        pass
def move_pad(pad):
    #moving left and right (velocity)
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_LEFT]:
        pad.velocity[0] = -5
    elif pressed_key[pygame.K_RIGHT]:
        pad.velocity[0] = 5
    else:
        pad.velocity[0] = 0
    
    #hitting the wall (depending on width of screen or specific design)
    if pad.pos[0] == 10 and pad.velocity[0] < 0:
        pad.velocity[0] = 0
    elif pad.pos[0] + pad.size == 790 and pad.velocity[0] > 0:
        pad.velocity[0] = 0

    #actual movement
    pad.pos += pad.velocity

def move(list_of_object: list = []):
    for i in list_of_object:
        if type(i) == objects.Pad:
            move_pad(i)
        elif True:
            pass
        else:
            pass

