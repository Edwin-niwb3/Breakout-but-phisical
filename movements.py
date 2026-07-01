import numpy as np
import pygame
import objects

def ball_collision(ball, object):
    ball_pos = ball.pos + ball.size/2
    object_pos = object.pos + object.size/2
    if type(object) == objects.Pad:
        if object.form == 'linear':
            #position of ball as a point in coordinate system of pad
            p = ball_pos - object_pos
            #distance
            d_1 = np.cos(object.facing_angle - np.pi/2)*(abs(p[1]-np.tan(object.facing_angle - np.pi/2)*p[0]))
            #all the same, but for width of pad
            d_2 = np.cos(object.facing_angle)*(abs(p[1]-np.tan(object.facing_angle)*p[0]))
            #detect collision and where it happens
            if d_1 <= object.thickness/2 + ball.size/2  and d_2 <= (object.size - object.thickness)/2:
                #up/down side collision
                #notice!! the positive rotation angle is no more conter clock wise.
                angle = - object.facing_angle
                rotate_matrix = np.array([[np.cos(angle),-np.sin(angle)],
                                        [np.sin(angle),np.cos(angle)]])
                flip_matrix = np.array([[0,1],
                                        [1,0]])
                ball.velocity = ball.velocity @ rotate_matrix @ flip_matrix
            elif d_2 <= (object.size - object.thickness)/2 + ball.size/2 and d_1 <= object.thickness/2:
                #left/right side collision
                pass
            # elif True:
            #     #corner collision
            #     pass
            # else:
                #plan 2
            #     ball.last_pos = np.array([d_1, d_2])

def move_pad(pad):
    #moving left and right (velocity)
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_LEFT]:
        pad.velocity[0] = -5
    elif pressed_key[pygame.K_RIGHT]:
        pad.velocity[0] = 5
    else:
        pad.velocity[0] = 0
    #rotation
    if pressed_key[pygame.K_a]:
        pad.rotate(0.01*np.pi)
    #hitting the wall (depending on width of screen or specific design)
    if pad.pos[0] == 10 and pad.velocity[0] < 0:
        pad.velocity[0] = 0
    elif pad.pos[0] + pad.size == 790 and pad.velocity[0] > 0:
        pad.velocity[0] = 0

    #actual movement
    pad.pos += pad.velocity

def move_ball(ball):
    ball.pos += ball.velocity

def move(list_of_object: list = []):
    for i in list_of_object:
        if type(i) == objects.Pad:
            move_pad(i)
        elif type(i) == objects.Ball:
            move_ball(i)
        else:
            pass

