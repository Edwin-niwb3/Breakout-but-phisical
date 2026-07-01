import pygame
import numpy as np
import objects
import movements
import illustrations

pygame.init()
running = True
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
canvas = np.zeros((600,800,3))
pad = objects.Pad([400,500], thickness = 5)
ball = objects.Ball([400,300], size = 10, velocity = np.array([0,3]))
list_of_objects = [pad,ball]

#main loop
while running:
    #control
    for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            running = False

    movements.ball_collision(ball, pad)
    #movement of everything
    movements.move(list_of_objects)

    #illustration
    canvas = np.zeros((600,800,3))
    illustrations.illustrate(screen, canvas, list_of_objects)
    # #swaped axes
    # canvas[pad.pos[1] : pad.pos[1] + pad.size, pad.pos[0] : pad.pos[0] + pad.size] = pad.get_graph()
    # surface = pygame.surfarray.make_surface(canvas.swapaxes(0,1))
    # screen.blit(surface, (0,0))
    pygame.display.flip()
    #FPS
    clock.tick(60)