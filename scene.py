from OpenGL.GL import * # type: ignore
from array import array
import ctypes as ct
import logging
import asset

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

log.info(f'Module {__name__}')

vertex = array('f', [
                    # positions              texture coords
                     1.0,  1.0, 0.0,        1.0, 0.0,     # top right
                     1.0, -1.0, 0.0,        1.0, 1.0,     # bottom right
                    -1.0, -1.0, 0.0,        0.0, 1.0,     # bottom left
                    -1.0,  1.0, 0.0,        0.0, 0.0])    # top left

indices = array('i', [
                    0, 1, 3,    # first triangle
                    1, 2, 3])     # second  

class Scene:

    def __init__(self, viewport, fragment_src, vertex_src) -> None:
        
        self.__fsrc = fragment_src
        self.__vsrc = vertex_src
        self.viewport=viewport
        log.info(f'GL_VERSION: {glGetString(GL_VERSION)}' 
              f'\tGL_SHADER_LANG_VERSION: {glGetString(GL_SHADING_LANGUAGE_VERSION)}')
       
        log.debug('Create buffers')
        self.array_object   = glGenVertexArrays(1)
        self.vertex_buffer  = glGenBuffers(1)       
        self.element_buffer = glGenBuffers(1)
        
        log.debug('Create texture')
        self.texture = d2_texture(self.viewport, None)

        log.debug('Create shaders')
        self.vertex_shader    = create_shader(self.__vsrc, GL_VERTEX_SHADER)
        self.fragment_shader  = create_shader(self.__fsrc, GL_FRAGMENT_SHADER)
        
        log.debug('Create program')
        self.id = create_programm(self.vertex_shader, self.fragment_shader)

        log.debug('Bind buffers')
        self.__bind()
        pass

    def __bind(self):

        glBindVertexArray(self.array_object)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        log.debug('GL_ELEMENT_ARRAY_BUFFER')
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.tobytes(), GL_STATIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        log.debug('GL_ARRAY_BUFFER')
        glBufferData(GL_ARRAY_BUFFER, vertex.tobytes(), GL_STATIC_DRAW)
        
        log.debug('Vertex Attrib Pointer 0')
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5*len(vertex), ct.c_void_p(0))
        glEnableVertexAttribArray(0)

        log.debug('Vertex Attrib Pointer 1')
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5*len(vertex), ct.c_void_p(3))
        glEnableVertexAttribArray(1)
        
        glUseProgram(self.id)
        glUniform1i(glGetUniformLocation(self.id, 'camera'), 0)
        glActiveTexture(GL_TEXTURE0)

        glBindVertexArray(0)
        


    def build(self, frame):

        #filter-apply()
        glViewport(0,0, self.viewport[0], self.viewport[1])
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.id)
        glBindVertexArray(self.array_object)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.viewport[0], self.viewport[1], 0, GL_RGB, GL_UNSIGNED_BYTE, frame)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindVertexArray(0)

        
    def __del__(self) -> None:
#TODO: create safe delete
        if self.texture > 0: glDeleteTextures(1, [self.texture])
        if self.fragment_shader > 0: 
            if self.id > 0: glDetachShader(self.id, self.fragment_shader)
            glDeleteShader(self.fragment_shader)
        
        if self.vertex_shader > 0: 
            if self.id > 0: glDetachShader(self.id, self.vertex_shader)
            glDeleteShader(self.vertex_shader)

        if self.id > 0: glDeleteProgram(self.id)

        glDeleteBuffers(1, [self.element_buffer])
        glDeleteBuffers(1, [self.vertex_buffer])
        glDeleteVertexArrays(1, [self.array_object])

        pass


def create_shader(file, type) -> int:

    src: asset.Source = asset.Source(file)
    if not src.is_opened(): return 0

    shader: int = glCreateShader(type)
    glShaderSource(shader, src.read())
    glCompileShader(shader)

    is_compiled = ct.c_int(0)
    glGetShaderiv(shader, GL_COMPILE_STATUS, ct.byref(is_compiled))
    
    if is_compiled.value == GL_FALSE:
        
        log.error(f'Could not compile\n {glGetShaderInfoLog(shader)}')
        glDeleteShader(shader)
        shader = 0

    return shader

def create_programm(vertex_shader, fragment_shader) -> int:

    if vertex_shader == 0 or fragment_shader == 0: return 0

    prog = glCreateProgram()
    glAttachShader(prog, vertex_shader)
    glAttachShader(prog, fragment_shader)
    glLinkProgram(prog)
    is_linked = ct.c_int()
    glGetProgramiv(prog, GL_LINK_STATUS, ct.byref(is_linked))

    if is_linked == GL_FALSE:
        log.error('Could not link program')
        glDeleteProgram(prog)
        prog=0
    return prog

def d2_texture(viewport, bytes) -> int:
    
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 
                     viewport[0], viewport[1], 0, GL_RGB, GL_UNSIGNED_BYTE, bytes)
    return tex
    