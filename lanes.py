"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Author: Caroline Ryu 
Date: December 21, 2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.
    """
    pass

    # Hidden attributes 
    
    # Attribute _tile: A tiling of one lane using one image
    # Invariant: _tile is a GTile
    #
    # Attribute _objs: A list of GImage attributes (obstacles) with specified
    # x and y position and the source image
    # Invariant: Each element of _objs is a GImage
    #
    # Attribute _safefrogs: A list of GImage attributes (frogheads) with
    # specified x and y position and the source image
    # Invariant: Each element of _objs is a GImage

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def gettile(self):
        """
        Returns the tile of the lane with specified widht, height, and the
        source file
        """
        return self._tile

    def getobjs(self):
        """
        Returns the list of GImage obstacles with specified x,y position and
        the source file
        """
        return self._objs

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self,item,width,l):
        """
        Initializes one lane of the window from the passed-down parameters.

        Parameter item: a passed down parameter from Level, referring to one lane
        Precondition: item is a dictionary

        Parameter width: a passed down parameter from Level, the width of a
        game in pixels
        Precondition: width is a non-negative float value

        Parameter l: a passed down parameter from Level, the bottom position
        of the tile that each lane is going to be drawn
        Precondition: l is a non-negative float value
        """
        self._objs = []
        self._tile = GTile(left = 0, bottom = l, width= width,
        height= GRID_SIZE, source = str(item['type'])+'.png')
        self._safefrogs = []

        if 'objects' in item:
            for pos in range(len(item['objects'])):
                self._objs.append(GImage
                (x=item['objects'][pos]['position']*GRID_SIZE+.5*GRID_SIZE,
                y=.5*GRID_SIZE+l,source=str(item['objects'][pos]['type'])+'.png'))

        if 'speed' in item:
            if item['speed'] < 0 :
                for element in range(len(item['objects'])):
                    self._objs[element].angle = 180
                    speed = item['speed']

    def update(self,dt,speed,width,buffer,frog):
        """
        Updates the lane for the next animation frame

        The main function of this update is moving obstacles in relation to the
        speed of the lane, wrapping around with the buffer attribute, and

        Parameter input: A valid user input
        Precondition: input is an instance of GInput

        Parameter dt: time in seconds since the last call to update
        Precondition dt: dt is a non-negative float
        """
        for obstacle in self._objs:
            obstacle.x = obstacle.x + dt*speed
            if speed < 0:
                if obstacle.x < (-buffer*GRID_SIZE):
                    d = -buffer*GRID_SIZE-obstacle.x
                    obstacle.x = width + buffer*GRID_SIZE -d
            if speed > 0:
                if obstacle.x > (buffer*GRID_SIZE+width):
                    d = obstacle.x - (buffer*GRID_SIZE+width)
                    obstacle.x = (-buffer*GRID_SIZE) + d

    def draw(self,view):
        """
        Instructs Python to draw the values in the body in the window.

        Parameter view: The view window
        Precondition: view is a GView
        """
        self._tile.draw(view)

        for element in self._objs:
            element.draw(view)

        for element in self._safefrogs:
            element.draw(view)


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.
    """
    pass


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.
    """
    def carcollision(self,frog):
        """
        Returns True if a car collides with the frog.

        Parameter frog: a frog to play the game
        Precondition: frog is a Frog object
        """
        if not frog is None:
            for obstacle in range(len(self._objs)):
                if self._objs[obstacle].collides(frog):
                    return True


class Water(Lane):
    """
    A class representing a waterway with logs.
    
    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    def onalog(self,frog):
        """
        Returns True if the log contains a center of the frog.

        This method loops over the obstacles to find the logs and if the
        log contains the center of the frog when the frog is still visible
        on the screen, it returns True.

        Parameter frog: a frog to play the game
        Precondition: frog is a Frog object
        """
        a = 'log1.png'
        b = 'log2.png'
        c = 'log3.png'
        d = 'log4.png'
        e = 'log5.png'
        for obstacle in self._objs:
            if obstacle.source is a or b or c or d or e:
                if not frog is None:
                    if obstacle.contains((frog.x,frog.y)):
                        return True

    def frogoffscreen(self,frog):
        """
        Returns True if the frog is off screen in the water lane(s).

        This method checks if the frog is off screen when it is being carried
        away by the log.

        Parameter frog: a frog to play the game
        Precondition: frog is a Frog object
        """

        a = frog.x<self._tile.left-GRID_SIZE//4
        b = frog.x>self._tile.width+GRID_SIZE//4
        if not frog is None:
            if a or b:
                return True


class Hedge(Lane):
    """
    A class representing the exit hedge.
    """
    def __init__(self,item,width,l):
        """
        Initializes one Hedge Lane.

        Parameter item: a passed down parameter from Lane, referring to one lane
        Precondition: item is a dictionary

        Parameter width: a passed down parameter from Lane, the width of a
        game in pixels
        Precondition: width is a non-negative float value

        Parameter l: a passed down parameter from Lane, the bottom position
        of the tile that each lane is going to be drawn
        Precondition: l is a non-negative float value
        """
        super().__init__(item,width,l)

    def contfrg(self,f):
        """
        Returns True if an empty exit contains the center of the frog.

        Parameter frog: a frog to play the game
        Precondition: f is a Frog object
        """
        for obstacle in self._objs:
            if not f is None:
                if obstacle.source != 'open.png':
                    if obstacle.contains((f.x, f.y)) and not self.usedexit(f):
                        self._safefrogs.append(GImage(x=f.x,y=f.y,
                        source = 'safe.png'))
                        return True

    def foropen(self,frog):
        """
        Returns True if the obstacle is an open and contains the center
        of the frog.

        This method loops over the obstacle in the lane and returns True if
        the obstacle is an open and contains the center of the frog.

        Parameter frog: a frog to play the game
        Precondition: frog is a Frog object
        """

        for obstacle in self._objs:
            if not frog is None:
                if obstacle.source == 'open.png':
                    if obstacle.contains((frog.x, frog.y)):
                        return True

    def usedexit(self,frog):
        """
        Returns True is the exit is already occupied by a blue frog.

        Parameter frog: a frog to play the game
        Precondition: frog is a Frog object
        """

        for frogs in self._safefrogs:
            if frogs.collides(frog):
                return True

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getsafefrogs(self):
        """
        Returns self._safefrogs, a list of GImages with blue frog (safe.png)
        as the source file and the positions of the frog.
        """
        return self._safefrogs
