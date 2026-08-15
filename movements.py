import numpy as np
import pygame
import objects

def ball_collision(ball, object):
    ball_pos = ball.pos + ball.size/2
    object_pos = object.pos + object.size/2
    #position of ball as a point in coordinate system of object
    p = ball_pos - object_pos
    if type(object) == objects.Pad:
        if object.form == 'linear':
            angle = object.facing_angle - np.pi/2
            reference_rotate_matrix = np.array([[np.cos(angle),np.sin(angle)],
                                                [-np.sin(angle),np.cos(angle)]])
            p = p @ np.transpose(reference_rotate_matrix)
            #collision
            if np.abs(p[0]) <= (object.lenth + ball.size)/2 and np.abs(p[1]) <= (object.thickness + ball.size)/2:
                v_pad = object.velocity @ np.transpose(reference_rotate_matrix)
                v_rotate_tan = p * object.angular_velocity @ np.array([[np.cos(np.pi/2),-np.sin(np.pi/2)],
                                                                        [np.sin(np.pi/2),np.cos(np.pi/2)]])
                v_ball = ball.velocity @ np.transpose(reference_rotate_matrix) - v_pad + v_rotate_tan
                v_ball_copy = np.copy(v_ball)

                #upper & lower surface
                if abs(p[0] - v_ball_copy[0]) <= (object.lenth)/2:  
                    #normal (orthogonal) collision
                    v_ball[1] = -v_ball[1]

                    #friction
                    
                    #error, should be fixed

                #left & right surface
                if abs(p[1] - v_ball_copy[1]) <= object.thickness/2:
                    #normal (orthogonal) collision
                    v_ball[0] = -v_ball[0]

                #corner collision, later
                else:
                    pass

                ball.velocity = (v_ball + v_pad) @ reference_rotate_matrix
            

def move_pad(pad):
    #moving left and right (velocity)
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_LEFT]:
        pad.velocity[0] = -3
    elif pressed_key[pygame.K_RIGHT]:
        pad.velocity[0] = 3
    else:
        pad.velocity[0] = 0

    #rotation
    if pressed_key[pygame.K_d]:
        pad.angular_velocity = 0.01* np.pi
        pad.rotate(pad.angular_velocity)
    elif pressed_key[pygame.K_a]:
        pad.angular_velocity = -0.01 * np.pi
        pad.rotate(pad.angular_velocity)
    else:
        pad.angular_velocity = 0

    #hitting the wall (depending on width of screen or specific design)
    if pad.pos[0] <= 10 and pad.velocity[0] < 0:
        pad.velocity[0] = 0
    elif pad.pos[0] + pad.size >= 790 and pad.velocity[0] > 0:
        pad.velocity[0] = 0

    #actual movement
    pad.pos += pad.velocity

def move_ball(ball):
    #hitting the wall (depending on width of screen or specific design)
    if ((ball.pos[0] < abs(ball.velocity[0]) and ball.velocity[0] < 0) 
        or (ball.pos[0] + ball.size > 800 - abs(ball.velocity[0]) and ball.velocity[0] > 0 )):

        ball.velocity[0] = -1* ball.velocity[0]
    elif ((ball.pos[1] < abs(ball.velocity[1]) and ball.velocity[1] < 0) 
        or (ball.pos[1] + ball.size > 600 - abs(ball.velocity[1]) and ball.velocity[1] > 0 )):
        ball.velocity[1] = -1* ball.velocity[1]

    #magnus effect
    angle = ball.magnus_effect_intensity * ball.angular_velocity
    R = np.array([[np.cos(angle), np.sin(angle)],
                  [-np.sin(angle), np.cos(angle)]])
    ball.velocity = ball.velocity @ R

    pressed_key = pygame.key.get_pressed()
    #for test
    if pressed_key[pygame.K_c]:
        ball.velocity = np.array([0.0,30.0])

    if (ball.velocity[0]**2 + ball.velocity[1]**2)**(1/2) >= 15:
        ball.velocity = ball.velocity / 2
        print('too fast')

    ball.pos += ball.velocity

def move(list_of_object: list = []):
    for i in list_of_object:
        if type(i) == objects.Pad:
            move_pad(i)
        elif type(i) == objects.Ball:
            move_ball(i)
        else:
            pass

