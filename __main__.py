"""
The primary application script for Froggit

    app.py      (the primary controller class)
    level.py    (the subcontroller for a single game level)
    models.py   (the model classes)
    consts.py   (the application constants)

    Fonts         (fonts to use for GLabel)
    Sounds        (sound effects for the game)
    Images        (image files to use in the game)
    JSON          (json files with the game data)

"""
from consts import *
from app import *

# Application code
if __name__ == '__main__':
    Froggit(width=GAME_WIDTH,height=GAME_HEIGHT).run()
