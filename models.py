"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Author: Caroline Ryu
Date: December 19, 2020
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.


class Frog(GImage):         # You will need to change this by Task 3
    """
    A class representing the frog
    """

    # INITIALIZER TO SET FROG POSITION
    def __init__(self,x,y):
        """
        initializes the position of the frog on the grid of x and y with
        the source image.

        Frog inherits the attributes from GImage and sets the angle to NORTH
        so that the frog is initially facing north.

        Parameter x: a intiial x position of the frog
        Precondition: x is a float value

        Parameter y: a intiial y position of the frog
        Precondition: y is a float value
        """
        super().__init__(x=x, y=y, source = FROG_IMAGE)
        self.angle = FROG_NORTh
