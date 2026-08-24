import pygame
import numpy as np
import objects
import movements
import illustrations
import random

pygame.init()
running = True
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
canvas = np.zeros((600,800,3))
pad = objects.Pad([400,500], lenth = 80, thickness = 10, friction_coefficient = 0.2)
ball = objects.Ball([400,100], size = 10, velocity = np.array([0.0,2.0]),
                    magnus_effect_intensity = 0.01)
brick = objects.Brick((200,100))
list_of_objects = [pad, ball, brick]
brick_quantity = 1
brick_quantity_max = 5

scoreboard = objects.Scoreboard([0,0], lenth = 150, thickness = 60)

game_over = 0

#main loop
while running:
    #control
    for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            running = False

    key_pressed = pygame.key.get_pressed()
    #Reset
    if key_pressed[pygame.K_ESCAPE]:
        game_over = 0
        pad = objects.Pad([400,500], lenth = 80, thickness = 10, friction_coefficient = 0.2)
        ball = objects.Ball([400,100], size = 10, velocity = np.array([0.0,2.0]),
                    magnus_effect_intensity = 0.01)
        brick = objects.Brick((200,100))
        list_of_objects = [pad, ball, brick]
        brick_quantity = 1
        brick_quantity_max = 5
        scoreboard = objects.Scoreboard([0,0], lenth = 150, thickness = 60)

    #test transformation
    # if key_pressed[pygame.K_t]:
    #     pad.change_size(pad.thickness - 1)
    # elif key_pressed[pygame.K_z]:
    #     pad.change_size(pad.thickness + 1)

    for i in list_of_objects:
        movements.ball_collision(ball, i)
    #movement of everything
    game_over += movements.move(list_of_objects)

    #spawn bricks and delete bricks
    brick_x_max = int(600/10 -1)
    brick_y_max = int(400/10 -1)
    while brick_quantity < brick_quantity_max:
        brick_x = random.randint(0,brick_x_max) * 10
        brick_y = random.randint(0,brick_y_max) * 10
        list_of_objects.append(objects.Brick(pos = (brick_x, brick_y)))
        brick_quantity += 1
    for i in list_of_objects:
        if type(i) == objects.Brick:
            if i.collided == 1:
                list_of_objects.remove(i)
                scoreboard.score += 1
                brick_quantity += -1


    #illustration
    canvas = np.zeros((600,800,3))
    illustrations.illustrate(screen, canvas, list_of_objects)
    scoreboard.scoreboard_render(screen)

    #for test, show the area of pad
    # p_1 = pad.pos.astype(int)
    # p_2 = (pad.pos + np.array([pad.size, 0])).astype(int)
    # p_3 = (pad.pos + np.array([pad.size, pad.size])).astype(int)
    # p_4 = (pad.pos + np.array([0, pad.size])).astype(int)
    # pygame.draw.lines(screen, 'white', 1, [p_1, p_2, p_3, p_4])

    #for test, show velocity
    # v = int((ball.velocity[0]**2 + ball.velocity[1]**2)**(1/2) * 1000) / 1000
    # print(v,ball.angular_velocity, end='\r')
    pygame.draw.line(screen, 'red', 
                     ball.pos + np.array([ball.size/2,ball.size/2]),
                     ball.pos + np.array([ball.size/2,ball.size/2]) + ball.velocity * 10)
    pygame.draw.circle(screen, 'blue' if ball.angular_velocity > 0 else 'red', (ball.pos + np.array([ball.size/2, ball.size/2])).astype(int),
                        int(abs(ball.angular_velocity)*50),1)

    if game_over:
        screen.fill('black')
        font = pygame.font.Font(None, 48)
        font1 = pygame.font.Font(None, 25)
        text_surface = font.render('Game Over', 0, 'white')
        text_surface1 = font1.render('Press \'ESC\' to reset the game',0,'white')
        screen.blit(text_surface, (300, 200))
        screen.blit(text_surface1, (300, 250))
        pass
    
    pygame.display.flip()
    #FPS
    clock.tick(60)