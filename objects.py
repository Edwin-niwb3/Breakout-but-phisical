import pygame
import numpy as np
class Object:
    def __init__(self, pos, size, facing_angle, velocity = np.array([0,0])):
        self.pos = np.array(pos).astype(float)
        self.size = size
        #the size of actuall picture should be always smaller than self.size.
        #since self.size is the size of get_graph(). And if self.size = 100,
        #the index 100 will be out of range in get_graph()
        self.facing_angle = facing_angle
        self.velocity = velocity
        self.phy_pos = self.pos ###yet useless

        #swaped axes
        self.rect_hit_box = pygame.Rect(self.pos[1],self.pos[0],self.size,self.size)
        self.points = np.array([[0,0]])
        self.points_int = self.points
    def get_graph(self):
        points_int = self.points.astype(int)
        pos_int = self.pos.astype(int)
        #swaped axes
        graph = points_int[:, [1,0]] + pos_int[[1,0]]
        return graph


class Pad(Object):
    def __init__(self, pos, size = 100, facing_angle = np.pi/2, form = "linear", thickness = 5, 
                 angular_velocity = 0, friction_coefficient = 1,
                 velocity = np.array([0,0])):
        super().__init__(pos, size, facing_angle, velocity)
        self.thickness = thickness

        #shape of the pad and the point set of it
        self.form = form

         #here, since point_x is defined by np.linspace(), we limit the upper and lower bound
        if self.form == "linear":
            points_x = np.array([ np.linspace(-(self.size/2 -self.thickness ), (self.size/2 -self.thickness), 100)] )
            points_x = np.tile(points_x, self.thickness)
            points_y = np.array([np.zeros(100 * self.thickness)])
            #Attention!!! Shape of point_x and points_y are (1,100*self.thickness).
            #They are 2D array, so that we can do transpose.
            for i in range(0,self.thickness):
                points_y[0, i*100: (i+1)*100] = - self.thickness/2 + i

        self.points = np.hstack((np.transpose(points_x),np.transpose(points_y)))
        self.points[:, 0] += self.size/2
        self.points[:, 1] += self.size/2
        self.points_int = self.points.astype(int)
        self.angular_velocity = angular_velocity

        #how strong is the rotation, which the pad brings to the ball
        #default 1: 100% friction
        self.friction_coefficient = friction_coefficient
        

    def rotate(self, angle):
        self.facing_angle += angle

        #it is transpose of rotational matrix, since we have row vectors
        rotation_matrix = np.array([[np.cos(angle),np.sin(angle)],
                                    [-np.sin(angle),np.cos(angle)]])
        
        self.points -= np.array([self.size/2,self.size/2])
        self.points = np.matmul(self.points, rotation_matrix)
        self.points += np.array([self.size/2,self.size/2])
        #Problem of position of Origin. fix later!!!!!!!!!!!!!!!!!!!!!!

    #get the actuall graph with colour
    def get_graph(self):
        return super().get_graph()


class Ball(Object):
    def __init__(self, pos, size, facing_angle = 0,velocity = np.array([0,0]), 
                 angular_velocity = 0, magnus_effect_intensity = 0.0001):
        super().__init__(pos, size, facing_angle, velocity)
        idx = np.indices((self.size,self.size))
        self.points = idx.reshape((2, -1)).transpose()
        self.points_centerized = self.points - self.size/2
        mask = (self.points_centerized[:,0]**2 + self.points_centerized[:,1]**2) ** (1/2) <= self.size/2
        self.points = self.points[mask]

        #for calculate collision
        self.last_pos = None
        self.angular_velocity = angular_velocity

        #It summarises a lot of physical parameters.
        self.magnus_effect_intensity = magnus_effect_intensity
    def get_graph(self):
        return super().get_graph()