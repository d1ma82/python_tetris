import traceback
import window
import gl_render
import tetris

WIDTH   = 480
HEIGHT  = 640
GameWindow : window.GLFW
GL_render : gl_render.GL_Render

def init():

    print('Init')
    global GameWindow
    GameWindow =  window.GLFW((WIDTH, HEIGHT), 'Tetris')          # Note: run this before use Opengl
    
    global GL_render
    GL_render = gl_render.GL_Render((WIDTH, HEIGHT))
    GameWindow.set_render(GL_render)

    listeners = tetris.Listeners()
    listeners.on_ground = lambda _: print("On ground sound")
    listeners.on_left   = lambda _: print("On left sound")
    listeners.on_right  = lambda _: print("On right sound")
    listeners.on_rotate = lambda _: print("On rotate sounnd")
    listeners.on_delete = lambda _: print("On delete sound")
    GL_render.attach_filterlist([tetris.Tetris((WIDTH, HEIGHT), listeners)])

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