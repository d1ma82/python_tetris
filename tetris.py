from typing import Callable
from enum import Enum
import numpy as np
import random
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
        
        self.__score                = 0
        self.__SZ                   = viewport[0]//Tetris.SQ_PER_LINE       # size of the square
        self.__viewport             = viewport
        self.__zeros                = np.zeros((viewport[0], viewport[1], 3), order='C', dtype=np.int8)
        self.__img                  = np.zeros((viewport[0], viewport[1], 3), order='C', dtype=np.int8)
        self.__current=0
        self.__previos=0
        self.__next=0          # mino key mem
        self.__game_over_flag         = False
        self.__minos:Map              = {}                                   # minos storage
        self.__listeners: Listeners   =   listeners

        log.info(f'SQ_PER_LINE {Tetris.SQ_PER_LINE}; SZ {self.__SZ}')

    
    
    def __create_mino_internal(self, type:Type, orientation:Orientation, color:tuple, pos_x, pos_y)->list[Brick]:
        
        mino = [Brick(type, orientation, color, Point(0,0))]*4
        
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
        pos_y = self.__SZ*4
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

    def frame(self)->np.ndarray: return self.__img

    def apply(self) -> None:

        if self.__current==0:
            self.__current = self.__create_mino()# if self.__next==0 else self.__next
             #self.__next = self.__create_mino()

        self.__previos = self.__current
        #self.__current = 0

        self.__img = np.copy(self.__zeros)

        for val in self.__minos.values():
            for brick in val:
                if brick.enabled: rectangle(self.__img, brick.tl, 
                                            Point(brick.tl.x+self.__SZ, brick.tl.y+self.__SZ),
                                            1, brick.color)
        np.save('img.bin', self.__img)
        # TODO: Test draw of line


def rectangle(img, pt1:Point, pt2:Point, border=2, color=[0]):
    """
        img: Input image where we want to draw rectangle:
        pt1: top left point (y, x)
        pt2: bottom right point
        border: border of line
        color: color of rectangle line,
        returns new image with rectangle.
       
    """
    p1 = pt1
    pt1 = Point(p1.y, p1.x)
    p2 = pt2
    pt2 = Point(p2.y, p2.x)
    b = int(np.ceil(border/2))
    cvalue = np.array(color)
    # get x coordinates for each line(top, bottom) of each side
    x11 = np.clip(pt1.x-b, 0, pt2.x)
    x12 = np.clip(pt1.x+b+1, 0, pt2.x)
    x21 = pt2.x-b
    x22 = pt2.x+b+1

    y11 = np.clip(pt1.y-b, 0, pt2.y)            
    y12 = np.clip(pt1.y+b+1, 0, pt2.y)  
    y21 = pt2.y-b
    y22 = pt2.y+b+1
    # right line
    img[x11:x22, y11:y12] = cvalue
    #left line
    img[x11:x22, y21:y22] = cvalue
    # top line
    img[x11:x12, y11:y22] = cvalue
    # bottom line
    img[x21:x22, y11:y22] = cvalue
       
    return img

            
