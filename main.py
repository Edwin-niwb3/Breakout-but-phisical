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
pad = objects.Pad([400,500], lenth = 80, thickness = 10, friction_coefficient = 0.2)
ball = objects.Ball([400,100], size = 10, velocity = np.array([0.0,4.0]),
                    magnus_effect_intensity = 0.01)
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
        pad.change_size(pad.thickness - 1)
    elif key_pressed[pygame.K_z]:
        pad.change_size(pad.thickness + 1)

    movements.ball_collision(ball, pad)
    #movement of everything
    movements.move(list_of_objects)
    
    #for test, show velocity
    # v = int((ball.velocity[0]**2 + ball.velocity[1]**2)**(1/2) * 1000) / 1000
    # print(v,ball.angular_velocity, end='\r')

    #illustration
    canvas = np.zeros((600,800,3))
    illustrations.illustrate(screen, canvas, list_of_objects)

    #for test, show the area of pad
    p_1 = pad.pos.astype(int)
    p_2 = (pad.pos + np.array([pad.size, 0])).astype(int)
    p_3 = (pad.pos + np.array([pad.size, pad.size])).astype(int)
    p_4 = (pad.pos + np.array([0, pad.size])).astype(int)
    pygame.draw.lines(screen, 'white', 1, [p_1, p_2, p_3, p_4])

    #for test, show velocity
    pygame.draw.line(screen, 'red', 
                     ball.pos + np.array([ball.size/2,ball.size/2]),
                     ball.pos + np.array([ball.size/2,ball.size/2]) + ball.velocity * 10)
    pygame.draw.circle(screen, 'blue' if ball.angular_velocity > 0 else 'red', (ball.pos + np.array([ball.size/2, ball.size/2])).astype(int),
                        int(abs(ball.angular_velocity)*50),1)
    
    pygame.display.flip()
    #FPS
    clock.tick(60)