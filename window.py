import glfw
from typing import Callable
from render import Render

key_press_event = Callable[['int', 'int'], None]   #key, action

class Events:
    on_key_press: key_press_event

class GLFW:
    
    def __init__(self, viewport, title) -> None:

        print(f"Create window {viewport}")
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        self.__window = glfw.create_window(viewport[0], viewport[1], title, None, None)
        self.__render = None
        glfw.make_context_current(self.__window)
        print("Done.")
        pass

    def set_event_listener(self, events: Events):
        self.__events=events
        if self.__events != None and self.__events.on_key_press != None:
            glfw.set_key_callback(self.__window, lambda _, p1, p2, p3, p4: self.__events.on_key_press(p1, p3))

    def set_render(self, render: Render): self.__render = render        # we cant add to init, cause window must create first

    def should_close(self):
        return glfw.window_should_close(self.__window)
    
    def close(self):
        glfw.set_window_should_close(self.__window, 1)

    def draw(self):
        
        self.__render.render()
        glfw.swap_buffers(self.__window)
        glfw.poll_events()
        pass

    def __del__(self):

        print("Destroy window")
        glfw.terminate()
