"""
Primary module for Froggit

This module contains the main controller class for the Froggit application. There
is no need for any additional classes in this module.  If you need more classes, 99%
of the time they belong in either the lanes module or the models module. If you are
unsure about where a new class should go, post a question on Piazza.

Author: Caroline Ryu (jr894)
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

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Level.
    Level should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

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

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        creates both the title (in attribute _title) and a message (in attribute
        _text) saying that the user should press a key to play a game.
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

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Level. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Level object _level to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_LOADING, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays the title and a simple message on the screen. The application
        remains in this state so long as the player never presses a key.

        STATE_LOADING: This is the state that creates a new level and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame (the amount of time to load
        the data from the file) before switching to STATE_ACTIVE. One of the
        key things about this state is that it resizes the window to match the
        level file.

        STATE_ACTIVE: This is a session of normal gameplay. The player can
        move the frog towards the exit, and the game will move all obstacles
        (cars and logs) about the screen. All of this should be handled inside
        of class Level (NOT in this class).  Hence the Level class should have
        an update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the frog after it was either killed
        or reached safety. The application switches to this state if the state
        was STATE_PAUSED in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over (all lives are lost or all frogs are safe),
        and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

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

        Every single thing you want to draw in this game is a GObject. To draw a
        GObject g, simply use the method g.draw(self.view). It is that easy!

        Many of the GObjects (such as the cars, logs, and exits) are attributes
        in either Level or Lane. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        those two classes.  We suggest the latter.  See the example subcontroller.py
        from the lesson videos.
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

        This helper method checks for a key press, and if there is one, changes
        the state to the next value.  A key press is when a key is pressed for
        the FIRST TIME. We do not want the state to continue to change as
        we hold down the key. The user must release the key and press it again
        to change the state.
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

        This helper method is called when the game enters STATE_LOADING. It
        loads the dictinoary form of the level json and the hitbox json as
        well as creates a Level object. It sets the width, height, and the frog's
        position and changes the state TO STATE_ACTIVE when complete.

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

        This helper method is called when the game enters STATE_PAUSED. Based
        on whether there is either no lives left (lose) or all the exits are
        filled (win), it either changes the state to STATE_COMPLETE or if not,
        displays the text 'PRESS 'C' TO CONTINUE'

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

        This helper method is called when the game enters STATE_COMPLETE. It
        determines whether the game was complete because the user lost or won
        the game. If the user lost, which can be determined by whether there
        are no lives left, the text 'YOU LOSE' is displayed and if the user
        won, which can be determined by whether all the exits are filled,
        the text 'YOU WIN'is displayed.

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

        This helper method is called when the game enters STATE_CONTINUE. It
        sets the position of the frog and then stops the text that is displayed
        when the game is paused from showing. It then changes back to
        STATE_ACTIVE.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._level.setfrog(self._frogx,self._frogy)
        self._pausetext = None
        self._state = STATE_ACTIVE

    def _stateactive(self, dt):
        """
        Handles the settings of the game when the game is in STATE_ACTIVE

        This helper method is called when the game enters STATE_ACTIVE. It
        updates the frame every 16 milliseconds. and if the frog is None, it
        brings the state to STATE_PAUSED.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._level.update(self.input,dt)
        if self._level.getfrog() is None:
            self._state = STATE_PAUSED

    def _stateinactive(self, dt):
        """
        Handles the settings of the game when the game is in STATE_INACTIVE

        This helper method is called when the game enters STATE_INACTIVE. It
        checks if the title text is there, and if there is one, it sets the
        text too.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._title != None:
            self._text.top = self._title.bottom
