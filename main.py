import traceback
import window
import render
import tetris

WIDTH   = 480
HEIGHT  = 640
GameWindow : window.GLFW
GL_render : render.GL_Render

def init():

    print('Init')
    global GameWindow
    GameWindow =  window.GLFW((WIDTH, HEIGHT), 'Tetris')          # Note: run this before use Opengl
    GameWindow.set_on_draw_listener(lambda: GL_render.render())

    global GL_render
    GL_render = render.GL_Render((WIDTH, HEIGHT))
    GL_render.attach_filterlist([tetris.Tetris((WIDTH, HEIGHT), tetris.Listeners())])

    pass

def loop():

    print("Begin loop")
    global GameWindow
    while not GameWindow.should_close():
        GameWindow.draw()
    pass

def clear():
    pass

def main():
    try:
        init()
        loop()
        
    except OSError as err:
        print("OS error:", err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}\n{traceback.print_tb(err.__traceback__)}")
    finally:
        clear()
    

if __name__ == '__main__':
    main()