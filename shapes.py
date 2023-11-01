import random
from enum import Enum

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

class MinoFactory():

    @staticmethod    
    def __create_mino_internal(type:Type, orientation:Orientation, color:tuple, pos_x, pos_y, sz)->list[Brick]:
        
        mino = [Brick(type, orientation, color, Point(0,0)),
                Brick(type, orientation, color, Point(0,0)),
                Brick(type, orientation, color, Point(0,0)),
                Brick(type, orientation, color, Point(0,0))]
        
        match type:
            case Type.LINE:
                match orientation:
                    case Orientation.O1:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x+sz, pos_y)
                        mino[2].tl = Point(pos_x+2*sz, pos_y)
                        mino[3].tl = Point(pos_x+3*sz, pos_y)
                                            
                    case Orientation.O2:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x, pos_y+2*sz)
                        mino[3].tl = Point(pos_x, pos_y+3*sz)

            case Type.Z:
                match orientation:
                    case Orientation.O1:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x+sz, pos_y)
                        mino[2].tl = Point(pos_x+sz, pos_y+sz)
                        mino[3].tl = Point(pos_x+2*sz, pos_y+sz)
                    case Orientation.O2:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x-sz, pos_y+sz)
                        mino[3].tl = Point(pos_x-sz, pos_y+2*sz)

            case Type.RZ:
                match orientation:
                    case Orientation.O1:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x-sz, pos_y)
                        mino[2].tl = Point(pos_x-sz, pos_y+sz)
                        mino[3].tl = Point(pos_x-2*sz, pos_y+sz)
                    case Orientation.O2:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x+sz, pos_y+sz)
                        mino[3].tl = Point(pos_x+sz, pos_y+2*sz)

            case Type.L:
                match orientation:
                    case Orientation.O1:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x-sz, pos_y+sz)
                        mino[3].tl = Point(pos_x-2*sz, pos_y+sz)
                    case Orientation.O2:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x, pos_y+2*sz)
                        mino[3].tl = Point(pos_x+sz, pos_y+2*sz)
                    case Orientation.O3:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y-sz)
                        mino[2].tl = Point(pos_x+sz, pos_y-sz)
                        mino[3].tl = Point(pos_x+2*sz, pos_y-sz)
                    case Orientation.O4:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x+sz, pos_y)
                        mino[2].tl = Point(pos_x+sz, pos_y+sz)
                        mino[3].tl = Point(pos_x+3*sz, pos_y+2*sz)

            case Type.RL:
                match orientation:
                    case Orientation.O1:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x+sz, pos_y+sz)
                        mino[3].tl = Point(pos_x+2*sz, pos_y+sz)
                    case Orientation.O2:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x-sz, pos_y)
                        mino[2].tl = Point(pos_x-sz, pos_y+sz)
                        mino[3].tl = Point(pos_x-sz, pos_y+2*sz)
                    case Orientation.O3:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x+sz, pos_y)
                        mino[2].tl = Point(pos_x+2*sz, pos_y)
                        mino[3].tl = Point(pos_x+2*sz, pos_y+sz)
                    case Orientation.O4:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x, pos_y+2*sz)
                        mino[3].tl = Point(pos_x-sz, pos_y+2*sz)
            case Type.T:
                match orientation:
                    case Orientation.O1:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x-sz, pos_y+sz)
                        mino[2].tl = Point(pos_x, pos_y+sz)
                        mino[3].tl = Point(pos_x+sz, pos_y+sz)
                    case Orientation.O2:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x, pos_y+2*sz)
                        mino[3].tl = Point(pos_x+sz, pos_y+sz)
                    case Orientation.O3:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x+sz, pos_y)
                        mino[2].tl = Point(pos_x+2*sz, pos_y)
                        mino[3].tl = Point(pos_x+sz, pos_y+sz)
                    case Orientation.O4:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x, pos_y+sz)
                        mino[2].tl = Point(pos_x, pos_y+2*sz)
                        mino[3].tl = Point(pos_x-sz, pos_y+sz)
            case Type.SQUARE:
                        mino[0].tl = Point(pos_x, pos_y)
                        mino[1].tl = Point(pos_x+sz, pos_y+sz)
                        mino[2].tl = Point(pos_x, pos_y+sz)
                        mino[3].tl = Point(pos_x+sz, pos_y+sz)

        return mino

    @staticmethod
    def create_mino(sq_per_line, sz)->list[Brick]: 

        type = Type(random.randrange(Type.LINE.value, Type.SQUARE.value))
        rgb = [255,0,0]
        random.shuffle(rgb)
        color = tuple(rgb)
        pos_x = random.randrange(4, sq_per_line-4)*sz
        pos_y = 0
        return MinoFactory.__create_mino_internal(type, Orientation.O1, color, pos_x, pos_y, sz)

