# Pygame
## Breakout but physical

It will be a game with physical effects, which is **inspired** by Breakout. Which means, it is not yet decided, if this game will be still Breakout or actually puzzle games etc.


Some points to note:
1. The first and second coordinate of Numpy's index and Pygame are different. Thus in main.py we can see, the canva array needs first a transpose, then it is able to be "brushed" onto the Screen. Therefore we always have to find a right time, to swap the axis after phisical calculation and before illustration. At these timepoints, there must be a comment.