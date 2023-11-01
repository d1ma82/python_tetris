from typing import Callable
import numpy as np
from PIL import Image
from PIL import ImageDraw
import logging
from filter import Filter
import importlib
import sett

log = logging.getLogger(__name__)
log.setLevel(sett.debug_level)
log.addHandler(sett.handler)

log.info(f'Module {__name__}')

imprt = importlib.import_module(sett.shapes_module)

Map = dict[int, list[imprt.Brick]]

listener = Callable[['int'], None]

class Listeners:
    on_left:listener; on_right:listener; on_rotate:listener; on_ground:listener; on_delete:listener

class Tetris(Filter):

    SQ_PER_LINE = 20
    SQ_PER_COL  = 26
    gen = (num+1 for num in range(1000))                    # mino id generator

    def __init__(self, viewport:tuple, listeners:Listeners) -> None:
        
        self.__score        = 0
        self.__SZ           = viewport[0]//Tetris.SQ_PER_LINE       # size of the square
        self.__viewport     = viewport
        self.__zeros        = np.zeros((viewport[1], viewport[0], 3), dtype=np.uint8)
        self.__img          = np.zeros((viewport[1], viewport[0], 3), dtype=np.uint8)
        self.__current=0
        self.__previos=0
        self.__next=0          # mino key mem
        self.__game_over_flag         = False
        self.__minos:Map              = {}                                   # minos storage
        self.__listeners: Listeners   =   listeners
        log.info(f'SQ_PER_LINE {Tetris.SQ_PER_LINE}; SZ {self.__SZ}')

    def __create_mino(self):

        id = next(Tetris.gen)
       # log.info(f'New mino id {id}; type {type}; color {color}; x {pos_x}')
        self.__minos[id] = imprt.Minos.create_mino(Tetris.SQ_PER_LINE, self.__SZ)
        log.info(f'New mino id {id};  {self.__minos[id]}; ')
        pass
    
    def __move_down(self)->bool:
        return True
    
    def __move_left(self):
        pass

    def __move_right(self):
        pass

    def __rotate(self):
        pass

    def __delete_lines(self, deleted:list):
        pass

    def frame(self)->np.ndarray[np.uint8]: return self.__img

    def apply(self) -> None:

        if self.__current==0:
            self.__current = self.__create_mino()# if self.__next==0 else self.__next
             #self.__next = self.__create_mino()

        self.__previos = self.__current
        #self.__current = 0

        img = Image.fromarray(self.__zeros)
        draw = ImageDraw.Draw(img)

        for val in self.__minos.values():
            for brick in val:
                if brick.enabled:
                    draw.rectangle([(brick.tl.x, brick.tl.y), (brick.tl.x+self.__SZ, brick.tl.y+self.__SZ)], fill = brick.color)
                    self.__img=np.asarray(img)
        # TODO: Test draw shapes