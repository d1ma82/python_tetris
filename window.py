import glfw

class GLFW:

    def __init__(self, width, height, title) -> None:

        print("Create window")
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        self.__window = glfw.create_window(width, height, title, None, None)
        self.__set_draw = False
        glfw.make_context_current(self.__window)
        print("Done")
        pass

    def set_on_draw_listener(self, draw_listener_fn):

        self.__draw_listener = draw_listener_fn
        self.__set_draw = True

    def should_close(self):
        return glfw.window_should_close(self.__window)
    
    def close(self):
        glfw.set_window_should_close(self.__window, 1)

    def draw(self):
        
        if self.__set_draw: self.__draw_listener()
        glfw.swap_buffers(self.__window)
        glfw.poll_events()
        pass

    def __del__(self):

        print("Destroy window")
        glfw.destroy_window(self.__window)
        glfw.terminate()
