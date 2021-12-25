"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

Author: Caroline Ryu 
Date: December 21, 2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *


class Level(object):
    """
    This class controls a single level of Froggit.
    """
    # HIDDEN ATTRIBUTES
    # Attribute: _width: a width of the game in pixels
    # Invariant: _width is a non-negative float value and is provided by the
    # JSON
    #
    # Attribute: _height: a height of the game in pixels
    # Invariant: _height is a non-negative float value and is provided by the
    # JSON
    #
    # Attribute: _lanes: # a list of lanes that will contain the lane objetcts
    # Invariant: _lanes is a list of lane objects of either Grass, Road, Water,
    # or Hedge
    #
    # Attribute: _livesc: a list of lives counter that will keep track of the
    # frogheads depending on number of lives left
    # Invariant: _livesc is a list of GImage objects or None if there are
    # no lives left
    #
    # Attribute: _cooldown: a cooldown attribute to avoid the frog rocketing
    # off screen
    # Invariant: _cooldown is a float value
    #
    # Attribute: _speed: a list of speeds for each lane in a given JSon
    # Invariant: _speed is a list of integers provided by the JSON
    #
    # Attribute: _buffer: a buffer size to avoid snapping
    # Invariant: _buffer is a non-negative interger provided by the JSON
    #
    # Attribute: _frog: a frog object to play in the game
    # Invariant: _frog is a Frog Object
    #
    # Attribute: _livest: a text to display 'Lives'
    # Invariant: _livest is a GLabel, or None if there is no message to display

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getwidth(self):
        """
        Returns self._width, the width of the game in pixels by multiplying
        GRID_SIZE to the width provided by the json
        """
        return self._width

    def getheight(self):
        """
        Returns self._height, the height of the game in pixels by multiplying
        GRID_SIZE to the height provided by the json
        """
        return self._height

    def getfrog(self):
        """
        Returns self._frog, a Frog object created in the initializer of the
        Level (this) class
        """
        return self._frog

    def setfrog(self,frogx,frogy):
        """
        Sets the x and y coordinates of the frog, a Frog object created in the
        initializer of the Level (this) class

        Parameter frogx: the x position of the frog to set to (in pixels)
        Precondition: frogx is a float

        Parameter frogy: the y position of the frog to set to (in pixels)
        Precondition: frogy is a float
        """
        self._frog = Frog(frogx,frogy)

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self, json):
        """
        Initializes the level settings to create a frog and the lanes from the
        given JSON

        Parameter json: A json file to set the level to
        Precondition: A valid json file containing all information to set the
        level in this game
        """
        # exactly 30 lines

        self._lanes = []
        self._livesc = []
        self._cooldown = 0
        self._width = json['size'][0]*GRID_SIZE
        self._height = json['size'][1]*GRID_SIZE
        self._speed = []
        self._buffer = json['offscreen']

        # going over each lane to add the corersponding lane objects (and speed
        # for Road and Water types) to self_lanes (and self._speed), respectively
        for pos in range(len(json['lanes'])):
            # an item refers to one lane
            item = json['lanes'][pos]
            l = GRID_SIZE * pos
            if json['lanes'][pos]['type'] == 'grass':
                self._lanes.append(Grass(item, self._width, l))
            elif json['lanes'][pos]['type'] == 'road':
                self._lanes.append(Road(item, self._width, l))
                self._speed.append(json['lanes'][pos]['speed'])
            elif json['lanes'][pos]['type'] == 'water':
                self._lanes.append(Water(item, self._width, l))
                self._speed.append(json['lanes'][pos]['speed'])
            elif json['lanes'][pos]['type'] == 'hedge':
                self._lanes.append(Hedge(item, self._width, l))

        # creating a frog object
        self._frog = Frog(json['start'][0]*GRID_SIZE+0.5*GRID_SIZE,
        json['start'][1]*GRID_SIZE+0.5*GRID_SIZE)

        # adding frogheads to self._livesc
        for element in range(FROG_LIVES):
            n = element + 1
            self._livesc.append(GImage(x=self._width-GRID_SIZE*n+0.5*GRID_SIZE,
            y= self._height+(GRID_SIZE//2),width = GRID_SIZE,height = GRID_SIZE,
            source = FROG_HEAD))

        # creating a label to display the lives
        self._livest = GLabel(text = "LIVES:",right = self._livesc[2].left,
        y =self._height+(GRID_SIZE//2),font_name = ALLOY_FONT,
        font_size = ALLOY_SMALL, linecolor = 'dark green')

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self, input, dt):
        """
        Updates the level for the next animation frame

        Parameter input: A valid user input
        Precondition: input is an instance of GInput

        Parameter dt: time in seconds since the last call to update
        Precondition dt: dt is a non-negative float
        """
        next = -1
        for lanes in (self._lanes):
            if isinstance(lanes,Water):
                next = next +1
                lanes.update(dt, self._speed[next],self._width, self._buffer,
                self._frog)
                if not self._frog is None:
                    if lanes.gettile().collides(self._frog):
                        if lanes.onalog(self._frog):
                            self._frog.x += self._speed[next]*dt
                            if lanes.frogoffscreen(self._frog):
                                self._frog = None
                                del self._livesc[0]
                        elif not lanes.onalog(self._frog):
                            self._frog = None
                            del self._livesc[0]
            elif isinstance(lanes,Road):
                next = next +1
                lanes.update(dt, self._speed[next],self._width, self._buffer,
                self._frog)
                if not self._frog is None:
                    if lanes.carcollision(self._frog):
                        del self._livesc[0]
                        self._frog = None
            elif isinstance(lanes,Hedge):
                if not self._frog is None:
                    if lanes.contfrg(self._frog) and not lanes.foropen(self._frog):
                        self._frog = None
        self.exitfill()
        self._whichkeypressed(input,dt)

    # DRAW METHOD TO DRAW THE FROG AND THE INDIVIDUAL LANES
    def draw(self,view):
        """
        Instructs Python to draw the values in the body in the window.

        Parameter view: The view window
        Precondition: view is a GView
        """
        for pos in self._lanes:
            pos.draw(view)
        if not self._frog is None:
            self._frog.draw(view)
        self._livest.draw(view)
        for pos in self._livesc:
            pos.draw(view)

    # PUBLIC NECESSARY HELPERS
    def nolives(self):
        """
        Returns True if there are no lives left. Returns False otherwise

        This method determines whether there are no lives left with the list
        that keeps track of how many lives are left. If this list if empty,
        it means there are no lives left, hence returning True. This method is
        used in app.py to determine if the user lost the game. That is, if this
        is True, the state will change to STATE_COMPLETE.
        """
        if self._livesc == []:
            return True
        else:
            return False

    def exitfill(self):
        """
        Returns True if the total number of blue frogs (filled exits) equals
        the total number of exits. Returns False otherwise

        This method is used in app.py to determine if the user won the game.
        That is, if this is True, the state will change to STATE_COMPLETE.
        """
        if self._numberoffrogs() == self._numberofexits():
            return True
        else:
            return False

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def _whichkeypressed(self, input, dt):
        """
        Calls the corresponding helper functions when each of the keys are
        pressed.

        Parameter input: A valid user input
        Precondition: input is an instance of GInput

        Parameter dt: time in seconds since the last call to update
        Precondition dt: dt is a non-negative float
        """
        if self._cooldown > dt:
            self._cooldown = self._cooldown - dt
        else:
            if input.is_key_down('left'):
                self._leftkeydown()
            elif input.is_key_down('right'):
                self._rightkeydown()
            elif input.is_key_down('up'):
                self._upkeydown()
            elif input.is_key_down('down'):
                self._downkeydown()

    def _leftkeydown(self):
        """
        Sets the motion of the frog accordingly when the 'left' key is pressed
        once

        This method makes sure that if the frog is near the edge of the window,
        it doens't go off screen. It allows the frog to move left a grid as
        long as the frog is not in an open where the movement is restricted.
        It also takes cooldown into consideration to not let the frog rocket off
        screen and make the frog face West when it's moving.
        """
        if self._frog.x <= GRID_SIZE:
            self._frog.x = self._frog.x
            self._frog.angle = FROG_WEST
        else:
            self._frog.x -= GRID_SIZE
            self._frog.angle = FROG_WEST
            for lanes in self._lanes:
                if isinstance(lanes,Hedge):
                    if self._frog is not None:
                        if lanes.gettile().collides(self._frog):
                            if not lanes.contfrg(self._frog):
                                self._frog.x += GRID_SIZE
                if isinstance(lanes,Road):
                    if self._frog is not None:
                        if lanes.carcollision(self._frog):
                            self._frog = None
                            del self._livesc[0]
                if isinstance(lanes,Water):
                    if self._frog is not None:
                        if lanes.gettile().collides(self._frog):
                            if not lanes.onalog(self._frog):
                                self._frog = None
                                del self._livesc[0]
        self._cooldown = FROG_SPEED

    def _rightkeydown(self):
        """
        Sets the motion of the frog accordingly when the 'right' key is pressed
        once

        This method makes sure that if the frog is near the edge of the window,
        it doens't go off screen. It allows the frog to move right a grid as
        long as the frog is not in an open where the movement is restricted.
        It also takes cooldown into consideration to not let the frog rocket off
        screen and make the frog face East when it's moving.
        """
        if self._frog is not None:
            if self._frog.x >= self._width - GRID_SIZE:
                self._frog.x = self._frog.x
                self._frog.angle = FROG_EAST
            else:
                self._frog.x += GRID_SIZE
                self._frog.angle = FROG_EAST
                for lanes in self._lanes:
                    if isinstance(lanes,Hedge):
                        if self._frog is not None:
                            if lanes.gettile().collides(self._frog):
                                if not lanes.contfrg(self._frog):
                                    self._frog.x -= GRID_SIZE
                    if isinstance(lanes,Road):
                        if self._frog is not None:
                            if lanes.carcollision(self._frog):
                                self._frog.angle = FROG_EAST
                                self._frog = None
                                del self._livesc[0]
                    if isinstance(lanes,Water):
                        if self._frog is not None:
                            if lanes.gettile().collides(self._frog):
                                if not lanes.onalog(self._frog):
                                    self._frog.angle = FROG_EAST
                                    self._frog = None
                                    del self._livesc[0]
                self._cooldown = FROG_SPEED

    def _upkeydown(self):
        """
        Sets the motion of the frog accordingly when the 'up' key is pressed
        once

        This method makes sure that if the frog is near the edge of the window,
        it doens't go off screen. It allows the frog to move up a grid as
        long as the frog is trying to enter a filled exit or a Hedge tile that
        isn't an exit. It sets the frog to None if it enters an unfilled exit.
        It also takes cooldown into consideration to not let the frog rocket off
        screen and make the frog face North when it's moving.
        """
        if not self._frog is None:
            if self._frog.y >= self._height - GRID_SIZE:
                self._frog.y = self._frog.y
                self._frog.angle = FROG_NORTH
            else:
                self._frog.y += GRID_SIZE
                self._frog.angle = FROG_NORTH
                for lanes in self._lanes:
                    if not self._frog is None:
                        if isinstance(lanes,Hedge):
                            if lanes.gettile().collides(self._frog):
                                if not lanes.contfrg(self._frog):
                                    if lanes.foropen(self._frog):
                                        self._frog.y = self._frog.y
                                    else:
                                        self._frog.y -= GRID_SIZE
                                else:
                                    self._frog = None
                            else:
                                self._frog.y = self._frog.y
                        if isinstance(lanes,Road):
                            if lanes.carcollision(self._frog):
                                self._frog = None
                                del self._livesc[0]
                        if isinstance(lanes,Water):
                            if lanes.gettile().collides(self._frog):
                                if not lanes.onalog(self._frog):
                                    self._frog = None
                                    del self._livesc[0]
                    self._cooldown = FROG_SPEED

    def _downkeydown(self):
        """
        Sets the motion of the frog accordingly when the 'down' key is pressed
        once

        This method makes sure that if the frog is near the edge of the window,
        it doens't go off screen. It allows the frog to move down a grid as
        long as the frog is trying to enter a filled exit or a Hedge tile that
        isn't an exit. It sets the frog to None if it enters an unfilled exit.
        It also takes cooldown into consideration to not let the frog rocket off
        screen and make the frog face South when it's moving.
        """
        if self._frog.y <= GRID_SIZE:
            self._frog.y = self._frog.y
            self._frog.angle = FROG_SOUTH
        else:
            self._frog.y -= GRID_SIZE
            self._frog.angle = FROG_SOUTH
            for lanes in self._lanes:
                if not self._frog is None:
                    if isinstance(lanes,Hedge):
                        if lanes.gettile().collides(self._frog):
                            if lanes.foropen(self._frog):
                                self._frog.y = self._frog.y
                                self._frog.angle = FROG_SOUTH
                            else:
                                self._frog.y += GRID_SIZE
                                self._frog.angle = FROG_SOUTH
                    if isinstance(lanes,Road):
                        if lanes.carcollision(self._frog):
                            self._frog = None
                            del self._livesc[0]
                    if isinstance(lanes,Water):
                        if lanes.gettile().collides(self._frog):
                            if not lanes.onalog(self._frog):
                                self._frog = None
                                del self._livesc[0]
        self._cooldown = FROG_SPEED

    def _numberofexits(self):
        """
        Returns the total number of exits in the level

        This method loops over each of the lanes and if that lane is a
        Hedge object, loop over the obstacle and adds the total number of exits
        to an accumulator if obstacle is an exit (and not an open). The
        accumulator is returned at the end to show the total number of exits
        and is later used to compare with the total number of filled exits
        to determine if the game is complete.
        """
        accum = 0
        for lanes in self._lanes:
            if isinstance(lanes,Hedge):
                for obstacle in lanes.getobjs():
                    if obstacle.source == 'exit.png':
                        accum += 1
        return accum

    def _numberoffrogs(self):
        """
        Returns the total number of blue frogs

        This method loops over each of the lanes and if that lane is a
        Hedge object, it adds the total number of blue frogs to an accumulator,
        which will be returned at the end to display the total number of
        blue frogs—that is, the number of filled exits.

        """
        numberoffrogs = 0
        for lanes in self._lanes:
            if isinstance(lanes,Hedge):
                numberoffrogs += len(lanes.getsafefrogs())
        return numberoffrogs
