import window
import render

WIDTH   = 480
HEIGHT  = 640
GameWindow = None
GL_render = None

def init():

    print('Init')
    global GameWindow
    GameWindow =  window.GLFW(WIDTH, HEIGHT, 'Tetris')          # Note: run this before use Opengl
    global GL_render
    GL_render = render.GL_Render(WIDTH, HEIGHT)
    GameWindow.set_on_draw_listener(lambda: GL_render.render())
    pass

def loop():

    print("Begin loop")
    global GameWindow
    while not GameWindow.should_close():
        GameWindow.draw()
    pass

def main():
    try:
        init()
        loop()
    except OSError as err:
        print("OS error:", err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    else:
        return
    

if __name__ == '__main__':
    main()