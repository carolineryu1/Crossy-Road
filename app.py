"""
Primary module 

Author: Caroline Ryu
Date: December 21, 2020
"""
from consts import *
from game2d import *
from level import *
import introcs

from kivy.logger import Logger


# PRIMARY RULE: Froggit can only access attributes in level.py via getters/setters
# Froggit is NOT allowed to access anything in lanes.py or models.py.


class Froggit(GameApp):
    """
    The primary controller class for the Froggit application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Level object

        Method draw displays the Level object and any other elements on screen

    The primary purpose of this class is managing the game state: when is the
    game started, paused, completed, etc. It keeps track of that in a hidden
    attribute

    Attribute view: The game view, used in drawing (see examples from class)
    Invariant: view is an instance of GView and is inherited from GameApp

    Attribute input: The user input, used to control the frog and change state
    Invariant: input is an instance of GInput and is inherited from GameApp
    """
    # HIDDEN ATTRIBUTES
    # Attribute _state: The current state of the game (taken from consts.py)
    # Invariant: _state is one of STATE_INACTIVE, STATE_LOADING, STATE_PAUSED,
    #            STATE_ACTIVE, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _level: The subcontroller for a  level, managing the frog and
    # obstacles
    # Invariant: _level is a Level object or None if no level is currently
    # active
    #
    # Attribute _title: The title of the game
    # Invariant: _title is a GLabel, or None if there is no title to display
    #
    # Attribute _text: A message to display to the player
    # Invariant: _text is a GLabel, or None if there is no message to display
    #
    # Attribute _pausetext: A message to display to the player when paused
    # Invariant: _pausetext is a GLabel, or None if there is no message to display
    #
    # Attribute _wintext: A message to display to the player when won
    # Invariant: _wintext is a GLabel, or None if there is no message to display
    #
    # Attribute _losetext: A message to display to the player when lost
    # Invariant: _losetext is a GLabel, or None if there is no message to display
    #
    # Attribute self._frogx: an x position of the frog to set to
    # Invariant: self._frogx is a float
    #
    # Attribute self._frogy: an x position of the frog to set to
    # Invariant: self._frogy is a float

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        """
        self._title = GLabel(text='FROGGIT',x=self.width//2,y= self.height//2,
        font_name=ALLOY_FONT,font_size=ALLOY_LARGE,linecolor='dark green')
        self._text = GLabel(text = "PRESS 'S' TO START",top=self._title.bottom,
        x=self.width//2,font_name=ALLOY_FONT,font_size=ALLOY_MEDIUM,
        linecolor='black')
        self._state = STATE_INACTIVE
        self._level = None
        self._pausetext = None
        self._losetext = None
        self._wintext = None

    def update(self,dt):
        """
        Updates the game objects each frame.
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._determineState()
        if self._state == STATE_INACTIVE:
            self._stateinactive(dt)
        if self._state == STATE_LOADING:
            self._stateloading(dt)
        if self._state == STATE_ACTIVE:
            self._stateactive(dt)
        if self._state == STATE_PAUSED:
            self._statepaused(dt)
        if self._state == STATE_CONTINUE:
            self._statecontinue(dt)
        if self._state == STATE_COMPLETE:
            self._statecomplete(dt)

    def draw(self):
        """
        Draws the game objects to the view.
        """

        if not self._text is None:
            self._text.draw(self.view)

        if not self._title is None:
            self._title.draw(self.view)

        if not self._level is None:
            self._level.draw(self.view)

        if not self._pausetext is None:
            self._pausetext.draw(self.view)

        if not self._losetext is None:
            self._losetext.draw(self.view)

        if not self._wintext is None:
            self._wintext.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """
        Determines the current state and assigns it to self.state
        """
        #adopted from the sample files
        # Determine the current number of keys pressed
        curr_keys = self.input.key_count

        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys == 0

        if change:
            if self.input.is_key_down('s') and self._state == STATE_INACTIVE:
                self._state = STATE_LOADING
                self._title = None
                self._text = None
            if self.input.is_key_down('c') and self._state == STATE_PAUSED:
                self._state = STATE_CONTINUE
        # Update last_keys
        self.lastkeys=curr_keys

    def _stateloading(self, dt):
        """
        Handles the settings of the game when the game is in STATE_LOADING
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        dictform = self.load_json(DEFAULT_LEVEL)
        self._level = Level(dictform)
        self.width = self._level.getwidth()
        self.height = self._level.getheight() + GRID_SIZE
        self._frogx = self._level.getfrog().x
        self._frogy = self._level.getfrog().y
        self._state = STATE_ACTIVE

    def _statepaused(self, dt):
        """
        Handles the settings of the game when the game is in STATE_PAUSED
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._level.nolives() is True or self._level.exitfill() is True:
            self._state = STATE_COMPLETE
        else:
            self._pausetext = GLabel(text = "PRESS 'C' TO CONTINUE",
            x = self.width//2, y= (self.height-GRID_SIZE)//2,
            width = self.width, height = GRID_SIZE, font_name = ALLOY_FONT,
            font_size = ALLOY_SMALL, linecolor = 'white',
            fillcolor = 'dark green')

    def _statecomplete(self, dt):
        """
        Handles the settings of the game when the game is in STATE_COMPLETE
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._level.nolives() is True:
            self._losetext = GLabel(text = "YOU LOSE", x = self.width//2,
            y= (self.height-GRID_SIZE)//2, width = self.width,
            height = GRID_SIZE, font_name = ALLOY_FONT,
            font_size = ALLOY_SMALL, linecolor = 'white',
            fillcolor = 'dark green')
        if self._level.exitfill() is True:
            self._losetext = GLabel(text = "YOU WIN", x = self.width//2,
            y= (self.height-GRID_SIZE)//2, width = self.width,
            height=GRID_SIZE,font_name=ALLOY_FONT,font_size=ALLOY_SMALL,
            linecolor = 'white', fillcolor = 'dark green')

    def _statecontinue(self, dt):
        """
        Handles the settings of the game when the game is in STATE_CONTINUE
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._level.setfrog(self._frogx,self._frogy)
        self._pausetext = None
        self._state = STATE_ACTIVE

    def _stateactive(self, dt):
        """
        Handles the settings of the game when the game is in STATE_ACTIVE
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._level.update(self.input,dt)
        if self._level.getfrog() is None:
            self._state = STATE_PAUSED

    def _stateinactive(self, dt):
        """
        Handles the settings of the game when the game is in STATE_INACTIVE
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._title != None:
            self._text.top = self._title.bottom
