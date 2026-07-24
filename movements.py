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
            if np.abs(p[0]) <= (object.size - object.thickness + ball.size)/2 and np.abs(p[1]) <= (object.thickness + ball.size)/2:
                v_pad = object.velocity @ np.transpose(reference_rotate_matrix)
                v_ball = ball.velocity @ np.transpose(reference_rotate_matrix) - v_pad
                v_rotate = 0
                #upper & lower surface
                if abs(p[0]) <= object.size - object.thickness:  
                    #normal (orthogonal) collision
                    v_rotate = np.abs(p[0]) * object.angular_velocity
                    v_ball[1] = -v_ball[1] + v_pad[1] + 2* v_rotate * (p[0]/abs(p[0]))

                    #friction
                    last_angular_velocity = ball.angular_velocity
                    ball.angular_velocity += (v_ball[0] / (ball.size/2) - last_angular_velocity) * object.friction_coefficient
                    v_ball[0] += (last_angular_velocity - ball.angular_velocity) * (ball.size/2)

                #left & right surface
                elif abs(p[1]) <= object.thickness:
                    v_ball[0] = -v_ball[0]
                    #error, fix later
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
    if ((ball.pos[0] - ball.size/2 < 10 and ball.velocity[0] < 0) 
        or (ball.pos[0] + ball.size/2 > 790 and ball.velocity[0] > 0 )):
        ball.velocity[0] = -1* ball.velocity[0]
    elif ((ball.pos[1] - ball.size/2 < 10 and ball.velocity[1] < 0) 
        or (ball.pos[1] + ball.size/2 > 590 and ball.velocity[1] > 0 )):
        ball.velocity[1] = -1* ball.velocity[1]

    #magnus effect
    delta_v = np.array([0,0])
    v_ball_3d = np.array([ball.velocity[0],ball.velocity[1],0])
    v_angular_3d = np.array([0,0,ball.angular_velocity])
    f_magnus = ((ball.size/2)**3) * ball.magnus_effect_intensity * (np.cross(v_angular_3d,v_ball_3d))
    ball.velocity += np.array([f_magnus[0],f_magnus[1]])
    #Velocity constantly increasing!!! Fix later with Verlet Integral

    pressed_key = pygame.key.get_pressed()
    #for test
    if pressed_key[pygame.K_c]:
        ball.velocity = np.array([0.0,10.0])


    ball.pos += ball.velocity

def move(list_of_object: list = []):
    for i in list_of_object:
        if type(i) == objects.Pad:
            move_pad(i)
        elif type(i) == objects.Ball:
            move_ball(i)
        else:
            pass

