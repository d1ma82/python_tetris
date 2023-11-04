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
    on_left     :  event
    on_right    :  event
    on_rotate   :  event 
    on_ground   :  event 
    on_delete   :  event
    on_game_over:  event 
    on_close    :  event
 
Map= dict[int, list[imprt.Brick]]

class Tetris(Filter):

    SQ_PER_LINE = 12
    gen = (num+1 for num in range(1000))                    # mino id generator

    def __init__(self, viewport:tuple, events:Events) -> None:
        
        self.__score        = 0
        self.__prev_score   = 0
        self.__SZ           = viewport[0]//Tetris.SQ_PER_LINE       # size of the square
        self.__viewport     = viewport
        self.__zeros        = np.zeros((viewport[1], viewport[0], 3), dtype=np.uint8)
        self.__img          = np.zeros((viewport[1], viewport[0], 3), dtype=np.uint8)
        self.__current=0                                            # current mino key      
        self.__next=0                                               # next mino key
        self.__min_y=viewport[1]                                    # minimum y position from the bottom, used in delete rows
        self.__game_over_flag         = False
        self.__minos:Map              = {}                            # minos storage
        self.__events: Events   =   events
        log.info(f'SQ_PER_LINE {Tetris.SQ_PER_LINE}; SZ {self.__SZ}')

    def __create_mino(self)->int:

        id = next(Tetris.gen)
        self.__minos[id] = imprt.MinoFactory.create_mino(Tetris.SQ_PER_LINE, self.__SZ)
        log.info(f'New mino id {id};  {self.__minos[id]}; ')
        return id
    
    def close(self): self.__events.on_close(0)
    
    def move_down(self)->bool:

        if self.__current==0 or self.__game_over_flag: return False
        
        for c_brick in self.__minos[self.__current]:                                                         #loop bricks from cuurent
            if c_brick.tl.y+self.__SZ >= self.__viewport[1]: return False                                                    #If on the ground

            for key in self.__minos:
                if self.__current==key or self.__next==key: continue            #Ignore current and next minos

                for brick in self.__minos[key]:                                                 #loop bricks from mino storage
                    if brick.enabled and c_brick.tl.y+self.__SZ>=brick.tl.y:
                        if c_brick.tl.x==brick.tl.x and                          \
                           c_brick.tl.x+self.__SZ==brick.tl.x+self.__SZ and     \
                           c_brick.tl.y+self.__SZ==brick.tl.y: return False

        for brick in self.__minos[self.__current]: brick.tl.y += 1
        return True
    
    def move_left(self):

        if self.__current==0 or self.__game_over_flag: return

        for c_brick in self.__minos[self.__current]:
            if c_brick.tl.x==0: return

            for key in self.__minos:
                if self.__current==key or self.__next==key: continue

                for brick in self.__minos[key]:
                    if brick.enabled: 
                        if c_brick.tl.y<brick.tl.y:
                             if c_brick.tl.y+self.__SZ>brick.tl.y and      \
                                    c_brick.tl.y+self.__SZ<brick.tl.y+self.__SZ and     \
                                        c_brick.tl.x==brick.tl.x+self.__SZ: return
                        
                        elif c_brick.tl.y>brick.tl.y:
                             if  c_brick.tl.y<brick.tl.y+self.__SZ and              \
                                        c_brick.tl.x==brick.tl.x+self.__SZ: return
                             
                        elif c_brick.tl.y==brick.tl.y:
                             if c_brick.tl.y==brick.tl.y and               \
                                    c_brick.tl.y+self.__SZ==brick.tl.y+self.__SZ: return

        for brick in self.__minos[self.__current]: brick.tl.x -= self.__SZ
        self.__events.on_left(0)    

    def move_right(self):
        if self.__current==0 or self.__game_over_flag: return
        
        for c_brick in self.__minos[self.__current]:
            if c_brick.tl.x==self.__viewport[0]-self.__SZ: return

            for key in self.__minos:
                if self.__current==key or self.__next==key: continue

                for brick in self.__minos[key]:
                    if brick.enabled: 
                        if c_brick.tl.y<brick.tl.y:
                             if c_brick.tl.y+self.__SZ>brick.tl.y and      \
                                    c_brick.tl.y+self.__SZ<brick.tl.y+self.__SZ and     \
                                        c_brick.tl.x+self.__SZ==brick.tl.x: return
                        
                        elif c_brick.tl.y>brick.tl.y:
                             if  c_brick.tl.y<brick.tl.y+self.__SZ and              \
                                        c_brick.tl.x+self.__SZ==brick.tl.x: return
                             
                        elif c_brick.tl.y==brick.tl.y:
                             if c_brick.tl.y==brick.tl.y and               \
                                    c_brick.tl.y+self.__SZ==brick.tl.y+self.__SZ: return

        for brick in self.__minos[self.__current]: brick.tl.x += self.__SZ
        self.__events.on_right(0)

    def rotate(self):
        if self.__current==0 or self.__game_over_flag: return
        mino = imprt.MinoFactory.rotated(self.__minos[self.__current][0], self.__SZ)

        for c_brick in mino:
            if c_brick.tl.x>self.__viewport[0]-self.__SZ or c_brick.tl.x<0: return

            for key in self.__minos:
                if self.__current==key or self.__next==key: continue

                for brick in self.__minos[key]:
                    if not brick.enabled: continue

                    if  (brick.tl.x <= c_brick.tl.x <= brick.tl.x+self.__SZ) and              \
                        (brick.tl.y <= c_brick.tl.y <= brick.tl.y+self.__SZ): return
                    
                    if  (brick.tl.x <= c_brick.tl.x+self.__SZ <= brick.tl.x+self.__SZ) and     \
                        (brick.tl.y <= c_brick.tl.y+self.__SZ <= brick.tl.y+self.__SZ): return
                    
        self.__minos[self.__current] = mino
        self.__events.on_rotate(0)

    def __calc_min_line_from_bottom(self): 
        """
        Calc min y pos from the bottom, for current mino, and store in a class attrib
        """
        for brick in self.__minos[self.__current]:
                self.__min_y = min(self.__min_y, brick.tl.y)
        
        print(f'min line = {self.__min_y}')
    
    def __delete_lines(self, begin: int):

        deleted:list[imprt.Brick] = []
        for key in self.__minos:
            if key==self.__next: continue
            for brick in self.__minos[key]:
                if brick.enabled and brick.tl.y==begin: deleted.append(brick)

        if len(deleted)==Tetris.SQ_PER_LINE:

            self.__prev_score = self.__score
            self.__score+=1

            for brick in deleted: brick.enabled=False

            for key in self.__minos:
                if key==self.__next: continue

                for brick in self.__minos[key]:
                    if brick.enabled and brick.tl.y<begin: brick.tl.y+=self.__SZ

            self.__delete_lines(begin)
        else:
            if begin-self.__SZ > self.__min_y:
                self.__delete_lines(begin-self.__SZ)


    def __game_over(self):

        self.__game_over_flag = self.__min_y<=self.__SZ*2

    def frame(self)->np.ndarray[np.uint8]: return self.__img

    def apply(self):

        if self.__game_over_flag: return

        if self.__current==0:
            self.__current = self.__create_mino() if self.__next==0 else self.__next
            self.__next = self.__create_mino()

        if not self.move_down(): 
            
            self.__calc_min_line_from_bottom()
            self.__delete_lines(self.__viewport[1]-self.__SZ)

            self.__current = 0

            if self.__score > self.__prev_score: 
                print(f"Score {self.__score}")
                self.__events.on_delete(self.__score-self.__prev_score)

            self.__events.on_ground(0)
        
        self.__game_over()
        if self.__game_over_flag: self.__events.on_game_over(self.__score)

        img = Image.fromarray(self.__zeros)
        draw = ImageDraw.Draw(img)

        for val in self.__minos.values():
            for brick in val:
                if brick.enabled:
                    draw.rectangle((brick.tl.x, brick.tl.y, brick.tl.x+self.__SZ, brick.tl.y+self.__SZ), fill = brick.color)
        self.__img=np.asarray(img)
