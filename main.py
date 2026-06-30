import pygame
import numpy as np
import objects
import movements

pygame.init()
running = True
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
canvas = np.zeros((600,800,3))
pad = objects.Pad([400,500], thickness = 5)
list_of_objects = [pad]

#main loop
while running:
    #control
    for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            running = False

    #detecting collision
    movements.detect_collision()
    #actuall movement of everything
    movements.move(list_of_objects)

    #illustration
    canvas = np.zeros((600,800,3))
    #swaped axes
    canvas[pad.pos[1] : pad.pos[1] + pad.size, pad.pos[0] : pad.pos[0] + pad.size] = pad.get_graph()
    surface = pygame.surfarray.make_surface(canvas.swapaxes(0,1))
    screen.blit(surface, (0,0))
    pygame.display.flip()
    #FPS
    clock.tick(60)