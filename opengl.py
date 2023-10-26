import OpenGL.GL as ogl
import ctypes as ct
import asset

class Programm:

    def __init__(self, viewport, fragment, vertex) -> None:
        
        print('Create buffers')
        self.array_object   = ogl.glGenVertexArrays(1)
        self.vertex_buffer  = ogl.glGenBuffers(1)       
        self.element_buffer = ogl.glGenBuffers(1)
        print('Done')
        print('Create texture')
        self.texture          : ogl.GLuint = d2_texture(viewport, None)
        print(f'texture={self.texture}')
        print('Create shader')
        self.vertex_shader    : ogl.GLuint = create_shader(vertex, ogl.GL_VERTEX_SHADER)
        self.fragment_shader  : ogl.GLuint = create_shader(fragment, ogl.GL_FRAGMENT_SHADER)
        print(f'vertex={self.vertex_shader}, fragment={self.fragment_shader}')
        print('Create program')
        if self.vertex_shader == 0 or self.fragment_shader == 0 : 
            self.id=0
        else:        
            self.id = create_programm(self.vertex_shader, self.fragment_shader)
        print(f'program={self.id}')
        pass

    def __del__(self) -> None:
#TODO: create safe delete
        if self.texture > 0: ogl.glDeleteTextures(len(self.texture), self.texture)
        if self.fragment_shader > 0: 
            ogl.glDetachShader(self.id, self.fragment_shader)
            ogl.glDeleteShader(self.fragment_shader)
        
        if self.vertex_shader > 0: 
            ogl.glDetachShader(self.id, self.vertex_shader)
            ogl.glDeleteShader(self.vertex_shader)

        if self.id > 0: ogl.glDeleteProgram(self.id)

        ogl.glDeleteBuffers(1, self.element_buffer)
        ogl.glDeleteBuffers(1, self.vertex_buffer)
        ogl.glDeleteVertexArrays(1, self.array_object)

        pass


def create_shader(file, type) -> ogl.GLuint:

    src: asset.Source = asset.Source(file)
    if not src.is_opened(): return 0

    shader = ogl.glCreateShader(type)
    ogl.glShaderSource(shader, src.read())
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

def d2_texture(viewport, bytes)-> ogl.GLuint:
    
    tex = ogl.glGenTextures(1)
    ogl.glBindTexture(ogl.GL_TEXTURE_2D, tex)
    ogl.glTexParameteri(ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_WRAP_S, ogl.GL_CLAMP_TO_EDGE)
    ogl.glTexParameteri(ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_WRAP_T, ogl.GL_CLAMP_TO_EDGE)
    ogl.glTexParameteri(ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MIN_FILTER, ogl.GL_LINEAR)
    ogl.glTexParameteri(ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MAG_FILTER, ogl.GL_LINEAR)
    ogl.glTexImage2D(ogl.GL_TEXTURE_2D, 0, ogl.GL_RGB, 
                     viewport[0], viewport[1], 0, ogl.GL_RGB, ogl.GL_UNSIGNED_BYTE, bytes)
    return tex
    