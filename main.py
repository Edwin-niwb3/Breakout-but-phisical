import pygame
import numpy as np
import objects

pygame.init()
running = True
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
canvas = np.zeros((600,800))
pad = objects.Pad([0,0])

#main loop
while running:
    #control
    for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    pad.set_pos(mouse_pos)
    #illustration
    canvas = np.zeros((600,800,3))
    
    pad_graph = pad.get_graph()
    canvas[pad.pos_y : pad.pos_y + pad.size, pad.pos_x : pad.pos_x + pad.size] = pad_graph
    surface = pygame.surfarray.make_surface(canvas.swapaxes(0,1))
    screen.blit(surface, (0,0))
    pygame.display.flip()
    #FPS
    clock.tick(60)