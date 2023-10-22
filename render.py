import opengl as gl


class GL_Render:

    def __init__(self, width, height) -> None:
        
        self.__vertex = [
                            # positions              texture coords
                             1.0,  1.0, 0.0,        1.0, 0.0,     # top right
                             1.0, -1.0, 0.0,        1.0, 1.0,     # bottom right
                            -1.0, -1.0, 0.0,        0.0, 1.0,     # bottom left
                            -1.0,  1.0, 0.0,        0.0, 0.0]     # top left 

        self.__indices = [
                            0, 1, 3,    # first triangle
                            1, 2, 3]     # second  
        
                   
        self.__width = width
        self.__height = height
        print(f'GL_VERSION: {gl.ogl.glGetString(gl.ogl.GL_VERSION)}' 
              f'\tGL_SHADER_LANG_VERSION: {gl.ogl.glGetString(gl.ogl.GL_SHADING_LANGUAGE_VERSION)}')

        pass

    def render(self):

        print('Render')
        pass