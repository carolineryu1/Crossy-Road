"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

Author: Caroline Ryu (jr894)
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

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    pass
    # LIST ALL HIDDEN ATTRIBUTES HERE

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

        The initializer appends the position and the source image to the list
        of objects as well as turns the angle of the objects around if it's less
        than 0 to make sure it is going on the right direction. It also
        intializes a tile, a list of safe frogs (when the frog enters an exit),
        as well as a hitbox dictionary.

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

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass

    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    def carcollision(self,frog):
        """
        Returns True if a car collides with the frog.

        This method loops over the obstacles in self._objs and use collidse
        to check if the the collides as long as the frog is still visible
        on the screen.

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

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

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

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    def __init__(self,item,width,l):
        """
        Initializes one Hedge Lane.

        The initializer appends the position and the source image to the list
        of objects as well as turns the angle of the objects around if it's less
        than 0 to make sure it is going on the right direction. It also
        intializes a tile, a list of safe frogs (when the frog enters an exit),

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

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION

    # ANY ADDITIONAL METHODS


# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
