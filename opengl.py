import OpenGL.GL as ogl
import ctypes as ct
import asset

class Programm:

    def __init__(self, fragment, vertex) -> None:
        
        self.texture          : ogl.GLuint = 0
        self.vertex_shader    : ogl.GLuint = create_shader(vertex, ogl.GL_VERTEX_SHADER)
        self.fragment_shader  : ogl.GLuint = create_shader(fragment, ogl.GL_FRAGMENT_SHADER)
        
        if self.vertex_shader == 0 or self.fragment_shader == 0 : 
            print('Could not create program')
            return
        
        self.id               : ogl.GLuint = create_programm(self.vertex_shader, self.fragment_shader)
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

def create_programm(vertex_shader, fragment_shader)->ogl.GLuint:

    print('Create program')
    prog = ogl.glCreateProgram()
    ogl.glAttachShader(prog, vertex_shader)
    ogl.glAttachShader(prog, fragment_shader)
    ogl.glLinkProgram(prog)
    is_linked = ct.c_int()
    ogl.glGetProgramiv(prog, ogl.GL_LINK_STATUS, ct.byref(is_linked))

    if is_linked == ogl.GL_FALSE:
        print('Could not link program')
        ogl.glDeleteProgram(prog)
        prog=0
    else: print('Link ok')
    return prog
    