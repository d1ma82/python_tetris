import glfw
from render import Render

class GLFW:

    def __init__(self, viewport, title) -> None:

        print(f"Create window {viewport}")
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        self.__window = glfw.create_window(viewport[0], viewport[1], title, None, None)
        self.__is_set_render = False
        glfw.make_context_current(self.__window)
        print("Done.")
        pass

    def set_render(self, render: Render):

        self.__render = render
        self.__is_set_render = True

    def should_close(self):
        return glfw.window_should_close(self.__window)
    
    def close(self):
        glfw.set_window_should_close(self.__window, 1)

    def draw(self):
        
        if self.__is_set_render: self.__render.render()
        glfw.swap_buffers(self.__window)
        glfw.poll_events()
        pass

    def __del__(self):

        print("Destroy window")
        glfw.terminate()
