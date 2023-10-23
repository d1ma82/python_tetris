import OpenGL.GL as ogl
import ctypes as ct
import asset

class Programm:

    def __init__(self) -> None:
        
        self.id               : ogl.GLuint = 0
        self.texture          : ogl.GLuint = 0
        self.vertex_shader    : ogl.GLuint = 0
        self.fragment_shader  : ogl.GLuint = 0
        self.VAO              : ogl.GLuint = 0         # Vertex Array object
        self.VBO              : ogl.GLuint = 0         # Vertex Buffer Object
        self.EBO              : ogl.GLuint = 0         # Element Buffer Object

        pass

    def __del__(self) -> None:
        pass


def create_shader(file, type) -> ogl.GLuint:

    src: asset.Source = asset.Source(file)
    if not src.is_opened(): return 0

    shader : ogl.GLuint = ogl.glCreateShader(type)
    code = src.read()
    ogl.glShaderSource(shader, code)
    print('Compile shader')
    ogl.glCompileShader(shader)

    is_compiled = ct.c_int(0)
    ogl.glGetShaderiv(shader, ogl.GL_COMPILE_STATUS, ct.byref(is_compiled))
    
    if is_compiled.value == ogl.GL_FALSE:

        print(f'Could not compile\n {ogl.glGetShaderInfoLog(shader)}')
        ogl.glDeleteShader(shader)
        shader = 0
    else: print('Compile OK')

    return shader