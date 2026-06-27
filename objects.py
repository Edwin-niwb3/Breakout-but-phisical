import pygame
import numpy as np

class Pad:
    def __init__(self, pos, size = 100, facing_angle = 0, form = "linear"):
        self.pos = np.array(pos)
        self.pos_x = np.array(pos)[0]
        self.pos_y = np.array(pos)[1]
        self.size = size
        self.facing_angle = facing_angle

        #shape of the pad
        self.form = form
        graph = np.zeros((self.size,self.size,3)).astype(int)
        points_x = np.array([ np.linspace(-self.size/2,self.size/2)] )
        if form == "linear":
            points_y = np.array([np.zeros(50)])
        points = np.hstack((np.transpose(points_x),np.transpose(points_y))).astype(int)
        graph[points[:,0],points[:,1]] = [255,255,255]
        self.graph = graph

    def set_pos(self, pos: np.array):
        self.pos = pos
        self.pos_x = np.array(pos)[0]
        self.pos_y = np.array(pos)[1]

    def set_size(self, size: float = 100):
        self.size = size
