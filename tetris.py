import numpy as np
from typing import Callable
from PIL import Image, ImageDraw
import logging
import importlib
from filter import Filter
import sett

log = logging.getLogger(__name__)
log.setLevel(sett.debug_level)
log.addHandler(sett.handler)

log.info(f'Module {__name__}')

imprt = importlib.import_module(sett.shapes_module)

event = Callable[['int'], None]


class Events:
    on_left  :  event
    on_right :  event
    on_rotate:  event 
    on_ground:  event 
    on_delete:  event 
    on_close :  event
 
Map = dict[int, list[imprt.Brick]]

class Tetris(Filter):

    SQ_PER_LINE = 20
    SQ_PER_COL  = 26
    gen = (num+1 for num in range(1000))                    # mino id generator

    def __init__(self, viewport:tuple, events:Events) -> None:
        
        self.__score        = 0
        self.__SZ           = viewport[0]//Tetris.SQ_PER_LINE       # size of the square
        self.__viewport     = viewport
        self.__zeros        = np.zeros((viewport[1], viewport[0], 3), dtype=np.uint8)
        self.__img          = np.zeros((viewport[1], viewport[0], 3), dtype=np.uint8)
        self.__current=0        # current mino key
        self.__previos=0        
        self.__next=0           # next mino key
        self.__game_over_flag         = False
        self.__minos:Map              = {}                                   # minos storage
        self.__events: Events   =   events
        log.info(f'SQ_PER_LINE {Tetris.SQ_PER_LINE}; SZ {self.__SZ}')

    def __create_mino(self)->int:

        id = next(Tetris.gen)
        self.__minos[id] = imprt.MinoFactory.create_mino(Tetris.SQ_PER_LINE, self.__SZ)
        log.info(f'New mino id {id};  {self.__minos[id]}; ')
        return id
    
    def close(self): self.__events.on_close(0)
    
    def move_down(self)->bool:

        center = self.__SZ//2
        if self.__current==0 or self.__game_over_flag: 
            log.debug("Return cause game over or no current")
            return False

        for c_brick in self.__minos[self.__current]:                                                         #loop bricks from cuurent
            if c_brick.tl.y+self.__SZ >= self.__viewport[1]: 
                log.debug("Return cause on the ground")
                return False                                                    #If on the ground

            for key in self.__minos:
                if self.__current==key or self.__next==key: continue            #Ignore current and next minos

                for brick in self.__minos[key]:                                                 #loop bricks from mino storage
                    if brick.enabled and c_brick.tl.y+self.__SZ>=brick.tl.y:
                        if c_brick.tl.x+center>=brick.tl.x and                          \
                           c_brick.tl.x+center<=brick.tl.x+self.__SZ: 
                            log.debug("Return cause beign the other mino")
                            return False

        for brick in self.__minos[self.__current]: brick.tl.y += 1
        return True
    
    def move_left(self):

      #  center = self.__SZ//2
      #  if self.__current==0 or self.__game_over_flag: return
#
      #  for c_brick in self.__minos[self.__current]:
      #      log.debug("Return cause left side")
      #      if c_brick.tl.x<0:return
#
      #  for key in self.__minos:
      #      if self.__current==key or self.__next==key: continue
#
      #  for brick in self.__minos[key]:
      #      if brick.enabled and c_brick.tl.x-self.__SZ<brick.tl.x+self.__SZ: return
#
        self.__events.on_left(0)    
        pass

    def move_right(self):
        self.__events.on_right(0)
        pass

    def rotate(self):
        self.__events.on_rotate(0)
        pass

    def __delete_lines(self, deleted:list):

        self.__events.on_delete(0)
        pass

    def frame(self)->np.ndarray[np.uint8]: return self.__img

    def apply(self) -> None:

        if self.__current==0:
            self.__current = self.__create_mino()# if self.__next==0 else self.__next
             #self.__next = self.__create_mino()

        self.__previos = self.__current
        #self.__current = 0

        if not self.move_down(): self.__events.on_ground(0)

        img = Image.fromarray(self.__zeros)
        draw = ImageDraw.Draw(img)

        for val in self.__minos.values():
            for brick in val:
                if brick.enabled:
                    draw.rectangle((brick.tl.x, brick.tl.y, brick.tl.x+self.__SZ, brick.tl.y+self.__SZ), fill = brick.color)
                    self.__img=np.asarray(img)
        # TODO: Test draw shapes
