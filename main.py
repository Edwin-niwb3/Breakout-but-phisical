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
pad = objects.Pad([400,500], thickness = 10, friction_coefficient = 1)
ball = objects.Ball([400,100], size = 10, velocity = np.array([0.0,2.0]),
                    magnus_effect_intensity = 0.0002)
list_of_objects = [pad,ball]

#main loop
while running:
    #control
    for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            running = False

    #test transformation
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_t]:
        pad.thickness += 1
    elif key_pressed[pygame.K_z]:
        pad.thickness -= 1
    #fix later

    movements.ball_collision(ball, pad)
    #movement of everything
    movements.move(list_of_objects)
    
    #for test, show velocity
    v = int((ball.velocity[0]**2 + ball.velocity[1]**2)**(1/2) * 1000) / 1000
    print(v,ball.angular_velocity, end='\r')

    #illustration
    canvas = np.zeros((600,800,3))
    illustrations.illustrate(screen, canvas, list_of_objects)
    pygame.display.flip()
    #FPS
    clock.tick(60)