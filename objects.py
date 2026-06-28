import pygame
import numpy as np
class Object:
    def __init__(self, pos, size, facing_angle):
        self.pos = np.array(pos)
        self.size = size
        #the size of actuall picture should be always smaller than self.size.
        #since self.size is the size of get_graph(). And if self.size = 100,
        #the index 100 will be out of range in get_graph()
        self.pos_x = np.array(pos)[0]
        self.pos_y = np.array(pos)[1]
        self.phy_pos = self.pos      ###
        self.facing_angle = facing_angle

class Pad(Object):
    def __init__(self, pos, size = 100, facing_angle = np.pi/2, form = "linear", thickness = 5):
        super().__init__(pos, size, facing_angle)

        self.thickness = thickness

        #shape of the pad and the point set of it
        self.form = form
        
        #here, since point_x is defined by np.linspace(), we limit the upper and lower bound
        if form == "linear":
            points_x = np.array([ np.linspace(-(self.size/2 -thickness ), (self.size/2 -thickness), 100)] )
            points_x = np.tile(points_x, thickness)
            points_y = np.array([np.zeros(100 * thickness)])
            #Attention!!! Shape of point_x and points_y are (1,100*thickness).
            #They are 2D array, so that we can do transpose.
            for i in range(0,thickness):
                points_y[0, i*100: (i+1)*100] = - thickness/2 + i
                print(points_y)#For debug
        #here, x and y is swaped, because the coordinate systems in Numpy and Pygame are different
        self.points = np.hstack((np.transpose(points_y),np.transpose(points_x)))

        self.points_int = self.points.astype(int)

    def set_pos(self, pos: np.array):
        self.pos = pos
        self.pos_x = np.array(pos)[0]
        self.pos_y = np.array(pos)[1]

    def set_size(self, size: float = 100):
        self.size = size

    def rotate(self, angle):
        self.facing_angle += angle
        rotation_matrix = np.array([[np.cos(angle),-np.sin(angle)],
                                    [np.sin(angle),np.cos(angle)]])
        self.points = np.matmul(self.points, rotation_matrix)
        self.points_int = self.points.astype(int)

    #get the actuall graph with colour
    def get_graph(self):
        graph = np.zeros((self.size, self.size, 3))
        points_for_graph = self.points_int + 50 #make them all positive
        graph[points_for_graph[:,0], points_for_graph[:,1]] = [255,255,255]
        return graph