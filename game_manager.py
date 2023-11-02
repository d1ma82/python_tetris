from typing import Callable
from glfw import PRESS, KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, KEY_ESCAPE
from tetris import Tetris

game: Tetris = None

key_listener = Callable[['int', 'int'], None]   #key, action

def on_key( key: int, action: int):

    if action==PRESS:
        if key == KEY_LEFT:     game.move_left()
        elif key == KEY_RIGHT:  game.move_right()
        elif key == KEY_UP:     game.rotate()
        elif key == KEY_DOWN:   game.move_down()
        elif key == KEY_ESCAPE: game.close()