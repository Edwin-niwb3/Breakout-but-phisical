import pygame
import numpy as np

class Pad:
    def __init__(self, pos, size = 100, facing_angle = 0, form = "linear"):
        self.pos = np.array(pos)
        self.pos_x = np.array(pos)[0]
        self.pos_y = np.array(pos)[1]
        self.size = size
        self.facing_angle = facing_angle
        self.form = form
    def set_pos(self, pos: np.array):
        self.pos = pos
        self.pos_x = np.array(pos)[0]
        self.pos_y = np.array(pos)[1]

    def set_size(self, size: float = 10):
        self.size = size

    def get_graph(self, colour = [255,255,255]):
        A = np.zeros((self.size,self.size,3)).astype(int)
        x = np.arange(int(-self.size/2),int(self.size/2))
        y = np.arange(int(-self.size/2),int(self.size/2))
        if ((self.facing_angle <= np.pi/4 or self.facing_angle >= 7*np.pi/4) or
            (self.facing_angle >= 3*np.pi/4 or self.facing_angle <= 5*np.pi/4)):
            y = x * np.tan(self.facing_angle) // 1
        else:
            x = y / (np.cos(self.facing_angle)/np.sin(self.facing_angle)) // 1
        
        x = (x + int(self.size/2)).astype(int)
        y = (y + int(self.size/2)).astype(int)

        A[x,y] = colour

        return A