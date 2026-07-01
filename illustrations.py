import numpy as np
import pygame
import objects



def illustrate(screen, canva, list_of_objects):
    for i in list_of_objects:
        canva[i.get_graph()[:,0], i.get_graph()[:,1]] = [255,255,255]
    surface = pygame.surfarray.make_surface(canva.swapaxes(0,1))
    screen.blit(surface, (0,0))