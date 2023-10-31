from typing import Callable
from enum import Enum
import numpy as np
import random
from PIL import Image
from PIL import ImageDraw
import logging
from filter import Filter
import sett

log = logging.getLogger(__name__)
log.setLevel(sett.debug_level)
log.addHandler(sett.handler)

log.info(f'Module {__name__}')

random.seed()

Type = Enum('Type', ['LINE', 'Z', 'RZ', 'L', 'RL', 'T', 'SQUARE'])
Orientation = Enum('Orientation', ['O1', 'O2', 'O3', 'O4'])

class Point: 
    def __init__(self, x:int, y:int) -> None:
        self.x: int = x
        self.y: int = y
        pass

    def __str__(self) -> str:
        return f'x={self.x}; y={self.y}'

class Brick:
    
    def __init__(self, type, orientation, color, tl:Point) -> None:
        
        self.type: Type                 = type
        self.orientation: Orientation   = orientation
        self.color:tuple                = color
        self.tl: Point                  = tl              # top left point
        self.enabled                    = True

Map = dict[int, list[Brick]]

listener = Callable[['Type'], None]

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

    
    
    def __create_mino_internal(self, type:Type, orientation:Orientation, color:tuple, pos_x, pos_y)->list[Brick]:
        
        mino = [Brick(type, orientation, color, Point(0,0)),
                Brick(type, orientation, color, Point(0,0)),
                Brick(type, orientation, color, Point(0,0)),
                Brick(type, orientation, color, Point(0,0))]
        
        match type:
            case Type.LINE:
                match orientation:
                    case Orientation.O1:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x+self.__SZ, pos_y)
                        mino[2].tl = Point(pos_x+2*self.__SZ, pos_y)
                        mino[3].tl = Point(pos_x+3*self.__SZ, pos_y)
                    
                    case Orientation.O2:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+self.__SZ)
                        mino[2].tl = Point(pos_x, pos_y+2*self.__SZ)
                        mino[3].tl = Point(pos_x, pos_y+3*self.__SZ)

        return mino

    def __create_mino(self):

        id = next(Tetris.gen)
        type = Type.LINE #Type(random.randrange(Type.LINE.value, Type.SQUARE.value))
        rgb = [255,0,0]
        random.shuffle(rgb)
        color = tuple(rgb)
        pos_x = random.randrange(4, Tetris.SQ_PER_LINE-4)*self.__SZ
        pos_y = self.__SZ*5
        log.info(f'New mino id {id}; type {type}; color {color}; x {pos_x}')
        mino = self.__create_mino_internal(type, Orientation.O1, color, pos_x, pos_y)
        self.__minos[id] = mino
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