import scene as gl


class GL_Render:

    def __init__(self, width, height) -> None:    

        self.__viewport = (width, height)           
        self.__output = gl.Programm(self.__viewport, './shader/out.frag', './shader/out.vert')
        
        pass

    def render(self):

        print(f'Render {self.__viewport}')
        
        pass