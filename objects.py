import pygame
import numpy as np

def pad_render(pad):
    points_x = np.array([np.linspace(0, (pad.lenth), 100)] )
    points_x = np.tile(points_x, pad.thickness)
    points_y = np.array([np.zeros(100 * pad.thickness)])
    #Attention!!! Shape of point_x and points_y are (1,100* thickness).
    #They are 2D array, so that we can do transpose.
    for i in range(0,pad.thickness):
        points_y[0, i*100: (i+1)*100] = i

    pad.points = np.hstack((np.transpose(points_x),np.transpose(points_y)))
    pad.points[:, 0] += (pad.size - pad.lenth)/2
    pad.points[:, 1] += (pad.size - pad.thickness)/2
    pad.points_int = pad.points.astype(int)

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
    def __init__(self, pos, size = 100, facing_angle = np.pi/2, form = "linear",lenth = 20, thickness = 5, 
                 angular_velocity = 0, friction_coefficient = 1,
                 velocity = np.array([0,0])):
        super().__init__(pos, size, facing_angle, velocity)
        self.thickness = thickness
        self.lenth = lenth

        #shape of the pad and the point set of it
        # self.form = form
        #yet useless

        #render
        pad_render(self)

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

    # #for test
    # def change_size(self, thickness):
    #     self.thickness = thickness
    #     #render again
    #     pad_render(self)

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

class Brick(Object):
    def __init__(self, pos, size = 100, facing_angle = np.pi/2, lenth = 30, thickness = 20,
                 angular_velocity = 0, friction_coefficient = 0.8, collided = 0):
        super().__init__(pos, size, facing_angle)
        self.lenth = lenth
        self.thickness = thickness
        self.angular_velocity = angular_velocity
        self.friction_coefficient = friction_coefficient
        self.collided = 0
        #render
        pad_render(self)
        #Here we yet borrow pad_render(), later we might rename it to rectangle_render()
        pass