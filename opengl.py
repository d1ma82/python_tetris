import OpenGL.GL as ogl

class Programm:

    def __init__(self) -> None:
        
        self.id = 0
        self.texture = 0
        self.vertex_shader = 0
        self.fragment_shader = 0
        self.VAO = 0                    # Vertex Array object
        self.VBO = 0                    # Vertex Buffer Object
        self.EBO = 0                    # Element Buffer Object

        pass

    def __del__(self) -> None:
        pass


def create_shader(file, type):

    cstr = ''
    shader = ogl.glCreateShader(type)
    ogl.glShaderSource(shader, 1, cstr, None)